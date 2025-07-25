from mcp import ClientSession
import asyncio
from mcp.client.streamable_http import streamablehttp_client
from contextlib import asynccontextmanager,AsyncExitStack

class MCPClient:
    def __init__(self,url):
        self.url=url
        self.stack=AsyncExitStack()
        self.sess = None

    async def list_tools(self):
        response=(await self._sess.list_tools()).tools
        return response

    async def list_prompts(self):
        response=(await self._sess.list_tools()).tools
        return response    

    async def __aenter__(self):
        read,write,_=await self.stack.enter_async_context(
            streamablehttp_client(self.url)
        )

        self._sess= await self.stack.enter_async_context(ClientSession(read,write))
        await self._sess.initialize()
        return self


    async def __aexit__(self,*arg):
        await self.stack.aclose()    


async def main():        
    async with MCPClient("http://localhost:8000/mcp") as client:
        tools= await client.list_tools()
        print(tools)

asyncio.run(main())    