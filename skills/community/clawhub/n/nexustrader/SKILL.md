---
name: nexustrader
description: NexusTrader trading assistant. Query crypto balances, positions, prices, and place orders on Binance, Bybit, OKX, Bitget, HyperLiquid.
credentials:
  - name: NEXUSTRADER_API_KEYS
    description: "Exchange API keys in .keys/.secrets.toml (local file, not transmitted)"
    scope: "local_file"
    required: true
env:
  - name: NEXUSTRADER_MCP_URL
    description: "MCP server URL (default: http://127.0.0.1:18765/sse)"
    required: false
  - name: NEXUSTRADER_PROJECT_DIR
    description: "Path to NexusTrader-mcp project (default: ~/NexusTrader-mcp)"
    required: false
  - name: NEXUSTRADER_NO_AUTOSTART
    description: "Set to 1 to disable automatic daemon start"
    required: false
metadata:
  openclaw:
    requires:
      bins: ["python3", "uv"]
      python_packages: ["fastmcp"]
    credentials:
      - name: NEXUSTRADER_API_KEYS
        description: "Exchange API keys stored in NexusTrader-mcp project at .keys/.secrets.toml"
        scope: "local_file"
    network:
      - "127.0.0.1:18765 (local MCP server via SSE)"
    side_effects:
      - "Auto-start is DISABLED by default (NEXUSTRADER_NO_AUTOSTART=1). Set to 0 in .env to enable."
      - "If auto-start is enabled: starts nexustrader-mcp as a background daemon with exchange API key access"
      - "Reads .env and .keys/.secrets.toml from local NexusTrader-mcp project directory"
      - "Can execute real trades via create_order/cancel_order/modify_order (requires explicit user confirmation)"
---

# NexusTrader

Use the **exec** tool to run bridge.py. Do not write code or call external HTTP APIs directly.
bridge.py connects to a local MCP server at 127.0.0.1:18765 (SSE) — all exchange communication goes through that server.

## Security Considerations

This skill accesses your exchange API keys. Before using:

- API keys are stored in `{NEXUSTRADER_PROJECT_DIR}/.keys/.secrets.toml` — a local file, never transmitted by this skill.
- **Auto-start is disabled by default.** The skill will not start background processes unless you explicitly set `NEXUSTRADER_NO_AUTOSTART=0` in the skill's `.env` file.
- If auto-start is enabled, the NexusTrader-mcp daemon will run in the background and hold access to your API keys.
- **Start with testnet/demo keys.** Only use real keys after verifying the workflow in a sandbox.
- Orders require explicit user confirmation — verify your agent flow enforces this before live trading.
- See upstream docs for key setup: https://github.com/Quantweb3-com/NexusTrader-mcp

## Environment Variables

- `NEXUSTRADER_PROJECT_DIR` (optional, default: `~/NexusTrader-mcp`): Location of your NexusTrader-mcp project directory. Controls where `.keys/.secrets.toml` is read from.
- `NEXUSTRADER_NO_AUTOSTART` (default: `1`): Set to `0` to allow bridge.py to auto-start the MCP daemon when offline. Default `1` means you must start the server manually.
- `NEXUSTRADER_MCP_URL` (optional, default: `http://127.0.0.1:18765/sse`): MCP server address if running on a non-default port.

## Usage

**Get all balances:**
`exec {baseDir}/bridge.py get_all_balances`

**Get all positions:**
`exec {baseDir}/bridge.py get_all_positions`

**Get balance for one exchange:**
`exec {baseDir}/bridge.py get_balance --exchange=okx`

**Get ticker:**
`exec {baseDir}/bridge.py get_ticker --symbol=BTCUSDT-PERP.BINANCE`

**Get klines:**
`exec {baseDir}/bridge.py get_klines --symbol=BTCUSDT-PERP.BINANCE --interval=1h --limit=24`

**Get open orders:**
`exec {baseDir}/bridge.py get_open_orders --exchange=okx`

**Get position for one symbol:**
`exec {baseDir}/bridge.py get_position --symbol=BTCUSDT-PERP.OKX`

**Place order (confirm first):**
`exec {baseDir}/bridge.py create_order --symbol=BTCUSDT-PERP.BINANCE --side=BUY --order_type=MARKET --amount=0.001`

**Cancel order (confirm first):**
`exec {baseDir}/bridge.py cancel_order --symbol=BTCUSDT-PERP.BINANCE --order_id=123`

Symbol format: `BTCUSDT-PERP.OKX` / `ETHUSDT-SPOT.BYBIT`. Exchange names lowercase.

If exec returns `{"error": ...}` → explain in Chinese.
If server not running → tell user to start manually: `cd ~/NexusTrader-mcp && uv run nexustrader-mcp start`

For orders, always confirm with user before calling create_order/cancel_order/modify_order.
