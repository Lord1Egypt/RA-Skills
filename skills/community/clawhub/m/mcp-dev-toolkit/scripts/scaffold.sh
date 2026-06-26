#!/usr/bin/env bash
set -e

NAME="${1:?Usage: scaffold.sh <name> <python|typescript>}"
LANG="${2:?Specify python or typescript}"
DIR="$NAME-mcp-server"

mkdir -p "$DIR"

if [ "$LANG" = "python" ]; then
  cat > "$DIR/server.py" <<'PYEOF'
"""MCP Server: REPLACE_NAME"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json

server = Server("REPLACE_NAME")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="hello",
            description="Say hello",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "hello":
        return [TextContent(type="text", text=f"Hello, {arguments['name']}!")]
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    async def main():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())
    asyncio.run(main())
PYEOF
  sed -i "s/REPLACE_NAME/$NAME/g" "$DIR/server.py"
  cat > "$DIR/requirements.txt" <<'DEPS'
mcp>=1.0.0
DEPS

elif [ "$LANG" = "typescript" ]; then
  cat > "$DIR/package.json" <<JSONEOF
{
  "name": "$NAME-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "scripts": { "build": "tsc", "start": "node dist/index.js" },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": { "typescript": "^5.3.0", "@types/node": "^20.0.0" }
}
JSONEOF
  mkdir -p "$DIR/src"
  cat > "$DIR/src/index.ts" <<'TSEOF'
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "REPLACE_NAME", version: "1.0.0" });

server.tool("hello", { name: z.string() }, async ({ name }) => ({
  content: [{ type: "text" as const, text: `Hello, ${name}!` }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
TSEOF
  sed -i "s/REPLACE_NAME/$NAME/g" "$DIR/src/index.ts"
  cat > "$DIR/tsconfig.json" <<'TSCONF'
{
  "compilerOptions": {
    "target": "ES2022", "module": "Node16", "moduleResolution": "Node16",
    "outDir": "./dist", "rootDir": "./src", "strict": true, "esModuleInterop": true
  },
  "include": ["src"]
}
TSCONF
fi

echo "Scaffolded $LANG MCP server in $DIR/"
