---
name: playwright-mcp-automation
description: Launch and operate the Playwright MCP server to let agents browse real websites (login, search, checkout, dashboards) through structured tools. Use when the task requires interacting with live pages beyond simple fetches—e.g., filling ecommerce carts, downloading statements behind auth, capturing screenshots, or testing UI flows with Playwright automation.
---

# Playwright MCP Automation

## Overview
Use this skill whenever an agent must drive a real browser session via the Playwright MCP server. It covers standing up the MCP daemon, wiring it into your MCP client, and running reliable automation loops (login → navigate → act → verify). Pair these instructions with the upstream repo (<https://github.com/microsoft/playwright-mcp>) for the latest binaries.

**Bundled resources**
- [`references/setup.md`](references/setup.md) — launch recipes, flags, troubleshooting.
- [`references/tools.md`](references/tools.md) — quick lookup table for MCP tools.
- [`scripts/start_playwright_mcp.sh`](scripts/start_playwright_mcp.sh) — opinionated launcher (persistent profile, sane timeouts). Override via env vars or CLI flags.

## Quick start (once per host)
1. **Install prerequisites**
   - Ensure Node.js ≥ 18.
   - Install Playwright browsers and system deps once:
     ```bash
     npx playwright install chromium
     # Linux only: installs missing libraries (x11, fonts, etc.)
     sudo npx playwright install-deps chromium
     ```
2. **Launch the MCP server**
   - Fast path: run `scripts/start_playwright_mcp.sh` from this skill directory. Override with `PWMCP_BROWSER`, `PWMCP_PORT`, etc.
   - Need custom flags? Copy-paste from [`references/setup.md`](references/setup.md) §2–5.
3. **Register the server with your agent**
   - Local STDIO client:
     ```json
     {
       "mcpServers": {
         "playwright": {
           "command": "npx",
           "args": ["@playwright/mcp@latest", "--browser=chromium", "--user-data-dir=/home/ai/.cache/playwright/mcp-profile", "--allowed-hosts=*", "--snapshot-mode=incremental"]
         }
       }
     }
     ```
   - Remote HTTP transport: expose `--port`/`--host` then set `"url": "http://HOST:PORT/mcp"`.
4. **Sanity check**
   - Call `browser_navigate` to `https://example.com`, then `browser_snapshot`. If the tree renders, automation is ready.

## Core workflow
Follow this loop for every task. Refer to [`references/tools.md`](references/tools.md) for exact tool signatures.

### 1. Plan & prep
- Clarify success criteria (e.g., "reach checkout confirmation", "download CSV").
- Decide on headed vs headless mode. Use headed when debugging CAPTCHAs/visual states.
- Make sure secrets (login cookies, OTP hooks) are available. If not, fall back to manual storage-state provisioning.

### 2. Navigate & observe
1. `browser_navigate` to the starting URL.
2. Immediately `browser_snapshot` to capture the accessibility tree.
3. If layout depends on viewport/device, adjust via launch flags (`--device`, `--viewport-size`) or call `browser_resize`.

### 3. Interact deterministically
Use semantic tools whenever possible:
- Inputs/buttons: `browser_click`, `browser_type`, `browser_fill_form`.
- Dropdowns: `browser_select_option`.
- Dynamic menus/tooltips: `browser_hover` → `browser_wait_for`.
- Multi-step flows (wizards, carts): after every step, `browser_snapshot` + assert expected text before proceeding.
- When markup lacks good roles, enable `--caps=vision` and fall back to `browser_mouse_*` tools, but only as a last resort.
- For brittle sequences (e.g., injecting JS, intercepting fetch), wrap logic inside `browser_run_code`:
  ```js
  async (page) => {
    await page.waitForSelector('text=Place order');
    await page.getByRole('button', { name: 'Place order' }).click();
    return await page.getByTestId('order-number').innerText();
  }
  ```

### 4. Handle waits & retries
- Prefer `browser_wait_for` with `text` / `textGone` over arbitrary sleeps.
- On timeout, fetch a fresh snapshot, confirm element existence, then retry once before escalating.
- Capture console/network logs (`browser_console_messages`, `browser_network_requests`) to debug API errors or CSP blocks.

### 5. Verify & capture artefacts
- Collect evidence via `browser_snapshot` and, if needed, `browser_take_screenshot` or `browser_pdf_save` (enable `--caps=pdf`).
- For multi-tab flows, list tabs via `browser_tabs` and ensure the correct tab is selected before final actions.
- Always `browser_close` at the end of unattended runs to release the browser.

## Authentication & state strategies
1. **Persistent profile (default script)**
   - Keeps cookies/localStorage inside `PWMCP_PROFILE`. Great for daily automations.
   - Rotate profile path per task to avoid cross-site contamination.
2. **Storage-state bootstrap**
   - Use Playwright CLI or manual login to create `storage.json`. Launch with `--storage-state=/path/to/storage.json` (see setup reference §4).
   - Update file whenever passwords change.
3. **Secrets file**
   - Launch with `--secrets path/.env` so MCP can expose sensitive values via `secrets.get`. Include API keys or 2FA tokens there instead of SKILL files.
4. **Browser extension bridge**
   - When you must reuse an already-signed-in Chrome profile, install the Playwright MCP Bridge extension and launch with `--extension`. Follow upstream README for pairing.

## Resilience checklist
- **CAPTCHA / MFA**: Surface snapshots promptly so a human can intervene or provide MFA codes. Document fallback in your agent conversation.
- **Slow sites**: Increase `--timeout-action`/`--timeout-navigation`, or stage requests via `browser_wait_for { time }`.
- **Resource throttling**: Use headless mode and disable `--save-video`/`--save-trace` unless debugging.
- **Logging**: Save snapshots to files (`browser_snapshot filename`) for audit trails, especially when producing evidence (e.g., order confirmations).

## When to read the references/scripts
- Need launch flags, network rules, or troubleshooting? → Open [`references/setup.md`](references/setup.md).
- Need to recall exact tool names/parameters? → Check [`references/tools.md`](references/tools.md).
- Want a ready-to-run launcher? → Execute or adapt [`scripts/start_playwright_mcp.sh`](scripts/start_playwright_mcp.sh). Export env vars (`PWMCP_PORT`, `PWMCP_EXTRA="--headless"`) before running to tweak behavior.

Keep SKILL.md lean by offloading details to the references. Update references/scripts whenever the upstream Playwright MCP release adds new capabilities (vision, pdf, devtools, etc.).
