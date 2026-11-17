---
name: open-agent-search-setup
description: Install Open Agent Search skills and connect its local stdio MCP server to an AI agent using uv and managed Python. Use for initial installation or MCP connection troubleshooting.
---

# Set up Open Agent Search

Use the official npm or Python package `open-agent-search`. No paid search API key or account is required. Search queries and fetched URLs go to upstream providers and websites; running locally does not make those requests private.

Check `uv --version`. If missing, follow https://docs.astral.sh/uv/getting-started/installation/ for the user's OS. Use an isolated environment with managed Python 3.12:

```sh
uvx --python 3.12 --from open-agent-search==1.0.4 oas-mcp
```

Alternatively, with Node.js 22+ and uv installed, use `npx --yes open-agent-search@1.0.4 mcp` or install `open-agent-search@1.0.4` with npm and run `oas-mcp`. The npm launcher still requires uv and uses the same managed Python package. Its `--version` and `--help` work without starting Python. `OPEN_AGENT_SEARCH_UVX` can select an absolute uvx path.

The first launch downloads Python if needed and dependencies. The Python entry point is a stdio server, not a CLI that prints search results or a `--help` check. Let the MCP client manage its lifetime.

For a plugin installation, the bundled MCP manifest already supplies this command. Otherwise add a server named `open-agent-search` with command `uvx` and args `["--python", "3.12", "--from", "open-agent-search==1.0.4", "oas-mcp"]` to the current client's supported MCP configuration. Merge that entry and preserve all other servers and settings. If the client cannot find `uvx`, resolve its absolute executable path. Do not wrap stdio with commands that print to stdout.

Install the setup and usage skills for the current agent:

```sh
npx --yes skills add Jayanth-MKV/open-agent-search --skill open-agent-search-setup open-agent-search --agent codex --copy --yes
```

Replace `codex` with the current agent's supported identifier and default to project scope. A plugin supplies both skills, so skip duplicate installation. If Node.js is unavailable, copy only these two repository skill directories into the client's supported skills directory, checking existing destinations before replacing them.

Verify through the MCP client: initialize, list tools, and confirm `search_web`, `search_images`, `search_videos`, `search_news`, `search_books`, `search_everything`, `fetch_content`, and `fetch_multiple_contents`. Run one short web search for a non-sensitive query. Distinguish connection success from an upstream search failure; include the actual error and avoid repeated retries. If tools become available only after a restart, state that verification is still pending.

HTTP hosting is optional. `uv tool install --python 3.12 open-agent-search==1.0.4` exposes `open-agent-search`; the npm command is `open-agent-search serve`. Both listen on all interfaces at port 8000 and mount HTTP MCP at `/ai/mcp`. Do not start HTTP hosting or deploy a service for a task that only asks for local MCP tools.
