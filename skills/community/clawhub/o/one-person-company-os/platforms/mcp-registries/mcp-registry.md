# MCP Registry Submission

Package: One Person Company OS

Version: 1.0.3

Server:

- transport: stdio
- command: `python3`
- args: `platforms/mcp-server/server.py`
- metadata: `platforms/mcp-server/server.json`

Description:

One Person Company OS gives MCP clients a local execution layer for a solo founder's operating cockpit. It supports workspace preflight checks, business initialization, focus updates, artifact generation, and release validation.

Submission requirement:

- publisher namespace/auth
- public repository URL
- package metadata from `server.json`
- safety statement that all persistent writes stay inside the founder-approved workspace

Do not mark as published until the official MCP Registry listing or version API record is visible.
