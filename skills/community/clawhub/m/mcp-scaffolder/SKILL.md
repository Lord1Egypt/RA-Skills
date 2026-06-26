---
name: mcp-scaffolder
description: Scaffolds a new MCP server from a one-line description. 
  Generates folder structure, typed tool definitions, transport config, 
  claude mcp add snippet, and README with env var documentation. 
  Use when: user says "create an MCP server", "scaffold an MCP server", 
  or "build a new MCP tool for Claude Code".
---

# MCP Scaffolder Skill

When the user describes an MCP server they want to build, scaffold it completely.

## What to Generate

1. Folder structure
   - /src/index.ts        — server entry point
   - /src/tools/          — one file per tool
   - /package.json        — with @modelcontextprotocol/sdk dependency
   - /tsconfig.json       — standard TS config
   - /.env.example        — all required env vars documented
   - /README.md           — setup instructions

2. Server entry point (src/index.ts)
   - Import and register all tools
   - Set transport based on user intent:
     - stdio  → local tools, file system access, CLI utilities
     - HTTP   → remote servers, cloud APIs, services
   - Include server instructions field — used by Claude Code tool search

3. Tool definitions
   - Each tool gets its own file in /src/tools/
   - Include: name, description, inputSchema (zod or JSON Schema)
   - Add JSDoc comments explaining what the tool does and when Claude should call it

4. Claude Code config snippet
   Always output a ready-to-paste config block:

   For stdio:
   {
     "mcpServers": {
       "<server-name>": {
         "type": "stdio",
         "command": "node",
         "args": ["<absolute-path>/build/index.js"],
         "env": { "<ENV_VAR>": "your-value-here" }
       }
     }
   }

   For HTTP:
   {
     "mcpServers": {
       "<server-name>": {
         "type": "http",
         "url": "http://localhost:3000/mcp"
       }
     }
   }

5. README
   - What the server does
   - Prerequisites
   - All env vars with descriptions
   - Build and run instructions
   - How to add to Claude Code

## Rules

- Never use SSE transport — it is deprecated, use HTTP instead
- Always include the server instructions field in the entry point
- Keep tool descriptions specific — Claude Code uses these for tool search
- Flag any required env vars in .env.example with a comment explaining what they are for
- Use TypeScript by default unless user specifies otherwise