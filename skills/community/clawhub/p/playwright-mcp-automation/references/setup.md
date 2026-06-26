# Playwright MCP Setup & Configuration

Use this cheat sheet whenever you need to spin up or adjust a Playwright MCP server for browser automation.

## 1. Prerequisites
- **Node.js 18+** with `npx`
- **Playwright browsers**: Run once per host:
  ```bash
  npx playwright install chromium
  sudo npx playwright install-deps chromium  # Linux only, pulls X11 libs/fonts
  ```
  (Or use `npx playwright install --with-deps` to fetch all engines.)
- **Client**: Any MCP-compatible agent (OpenClaw, Claude Code, Cursor, etc.).

## 2. Minimal launch command
```bash
npx @playwright/mcp@latest --browser=chromium --headless --allowed-hosts=* --snapshot-mode=incremental
```
- Use `--headless` only when you do **not** need to watch the browser. Remove it for debugging.
- `--allowed-hosts=*` bypasses DNS rebinding protection for local experiments.
- `--snapshot-mode=incremental` keeps diffs small for LLM consumption.

## 3. Recommended persistent-profile command
Keeps login state (cookies/localStorage) between sessions.
```bash
npx @playwright/mcp@latest \
  --browser=chromium \
  --user-data-dir=$HOME/.cache/ms-playwright/mcp-chromium-profile \
  --allowed-hosts=* \
  --snapshot-mode=incremental \
  --timeout-action=8000 \
  --timeout-navigation=60000
```
Tips:
- Remove `--user-data-dir` to fall back to Playwright's default (also persistent).
- Add `--headless` for CI, omit it to watch the UI locally.

## 4. Isolated session template
Use when you want a fresh context every run.
```bash
npx @playwright/mcp@latest \
  --browser=chromium \
  --isolated \
  --storage-state=/path/to/storage.json \
  --snapshot-mode=incremental \
  --timeout-action=8000 \
  --timeout-navigation=60000
```
- Generate `storage.json` through a manual Playwright login (CLI or script) and check it into a secrets vault, not the repo.

## 5. Remote / HTTP transport
When agents run elsewhere, expose MCP over HTTP:
```bash
npx @playwright/mcp@latest --browser=chromium --port=8931 --host=0.0.0.0
```
Client config snippet:
```json
{
  "mcpServers": {
    "playwright": {
      "url": "http://<SERVER_IP>:8931/mcp"
    }
  }
}
```
Secure the port with a firewall or tunnel.

## 6. Common launch flags
| Flag | Purpose |
| --- | --- |
| `--device "iPhone 15"` | Emulate mobile UA, viewport, input. |
| `--viewport-size 1280x720` | Override default viewport. |
| `--grant-permissions geolocation,clipboard-read` | Pre-approve browser permissions. |
| `--codegen none` | Disable Playwright code suggestions if not needed. |
| `--caps vision` | Enable coordinate-based tools (`browser_mouse_*`). |
| `--caps pdf` | Enable `browser_pdf_save`. |
| `--shared-browser-context` | Reuse one context across multiple MCP clients. |
| `--secrets /path/.env` | Inject secrets accessible via `secrets.get`. |

## 7. Troubleshooting checklist
1. **“Browser not installed”** → Run `npx @playwright/mcp browser install chromium` or call `browser_install` tool.
2. **“403/host blocked”** → Add the target domain to `--allowed-hosts` or disable DNS rebinding checks via `*` (only locally!).
3. **Timeouts on slow sites** → Raise `--timeout-action` / `--timeout-navigation` or call `browser_wait_for` with explicit `time`.
4. **Service workers breaking flows** → Launch with `--block-service-workers` for deterministic page loads.
5. **Need to reuse existing Chrome profile** → Install the Playwright MCP Bridge extension and launch with `--extension` (Chrome/Edge only).

## 8. Reference config file
When your MCP client reads from JSON config, keep a reusable block like:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser=chromium",
        "--user-data-dir=/home/ai/.cache/playwright/mcp-profile",
        "--allowed-hosts=*",
        "--snapshot-mode=incremental",
        "--timeout-action=8000",
        "--timeout-navigation=60000"
      ]
    }
  }
}
```
Adjust `--allowed-hosts` before exposing beyond localhost.
