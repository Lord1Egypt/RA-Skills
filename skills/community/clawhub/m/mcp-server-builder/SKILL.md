---
name: "mcp-server-builder"
description: "Build MCP servers (Model Context Protocol) that wrap your data and tools — FastMCP template. Turn any Python function into an MCP tool. 100% lokal template — du vælger selv endpoints."
metadata: {"clawbot": {"requires": {"python3": true, "bins": ["python3"]}, "notes": "Template til at bygge MCP-servere — ingen faste endpoints, ingen API-nøgle."}}
---

# MCP Server Builder 🔧🤖

Turn your service/data into MCP tools — so ALL AI agents can use it.

## What you get

1. **fastmcp template** — wraps your endpoints as tools
2. **Test flow** — verify that the tools work
3. **Publishing** — where agents find your MCP server

## Quick start

```bash
pip install fastmcp
cp scripts/mcp_server.py .
# Add YOUR @mcp.tool() functions
python3 mcp_server.py   # runs the MCP server
```

## Template (scripts/mcp_server.py)

```python
from fastmcp import FastMCP
mcp = FastMCP("my-server")

@mcp.tool()
def get_data(symbol: str = "BTCUSD") -> dict:
    """Get data."""
    return _call("/v1/signals", {"symbol": symbol})
```

## Publishing

- ClawHub: skill that wraps the server
- MCP-Hive / MCP Market: submit the server URL (manual browser verification)

## Files

```
mcp-server-builder/
├── SKILL.md
└── scripts/
    └── mcp_server.py   # fastmcp template
```
---
