# RapidX Skills / CLI / MCP Best Practices

## Overview

RapidX is delivered as a complete Agent integration stack:

- **Skills** teach the Agent how to install, configure, choose CLI or MCP, run self-checks, and operate RapidX.
- **CLI** is the unified local runtime for atomic operations and also starts the MCP server through `rapidx mcp serve`.
- **MCP** is the structured tool surface for MCP-capable Agents and shares the same CLI/Core capabilities.

The best practice is not to make users memorize every command. Let the Agent install and read the skills first. Load the installed `ltp-rapidx-config` skill to configure CLI/MCP and run self-checks, then load `ltp-rapidx-trading` for queries, preview, submit, automation, and readback. Skill names are not shell commands.

Recommended flow:

```text
Install Skills
→ ltp-rapidx-config installs/configures CLI
→ configure credentials and API host
→ choose MCP_READY or CLI_ONLY_READY
→ run self-check
→ ltp-rapidx-trading uses MCP or CLI
→ preview before write
→ submit
→ readback and reconcile
```

## 1. Role Of Each Layer

| Layer | Role | Best Practice |
|---|---|---|
| Skills | Agent guidance | Install and read `ltp-rapidx-config` first, then use `ltp-rapidx-trading`. |
| CLI | Unified local runtime | Install from official npm and use `rapidx ... --json` for CLI-only Agents. |
| MCP | Structured tool interface | Start with `rapidx mcp serve`; MCP-capable Agents call `rapidx/*` tools directly. |
| Core | Shared implementation | CLI and MCP share schemas, API client, preview, automation, audit, and self-check. |

The MCP server is not a separate package. It is started by the CLI:

```bash
rapidx mcp serve
```

MCP tools should call the shared RapidX core directly. They should not shell out through temporary scripts, wrapper files, or `cd ... && node ...` command chains.

## 2. Recommended External User Flow

### Step 1: Install Skills

Users can install skills themselves, or send an executable instruction to their Agent.

Recommended instruction to send to the Agent:

```text
You are my Agent. Install the RapidX skills into the current workspace using the skill installation method supported by your Agent host.

Source repository:
https://github.com/LiquidityTech/ltp-rapidx-skill

Install both skills:
- ltp-rapidx-config
- ltp-rapidx-trading

After installation, load and follow the installed `ltp-rapidx-config` skill first. It is not a shell command. Use it to install or upgrade @liquiditytech/rapidx-cli from official npm, configure RapidX credentials, configure MCP if this host supports MCP, and run RapidX self-check.

Do not start market queries or trading until you can report one of:
- MCP_READY
- CLI_ONLY_READY
- NOT_VERIFIED
```

The exact installation command depends on the Agent host. Use the official RapidX docs or skill repository README for Codex, Claude Code, Cursor, Gemini CLI, OpenCode, OpenClaw, and Hermes.

### Step 2: Use Config Skill

The Agent should load and follow `ltp-rapidx-config` before any market query or trade. This is a skill-guided workflow, not a shell command named `ltp-rapidx-config`.

Config skill responsibilities:

1. Confirm the Agent workspace.
2. Install or upgrade `@liquiditytech/rapidx-cli` from official npm.
3. Configure credentials.
4. Configure MCP when the host supports MCP.
5. Run tool discovery.
6. Run read-only self-check.
7. Report `MCP_READY`, `CLI_ONLY_READY`, or `NOT_VERIFIED`.

### Step 3: Use Trading Skill

After config is verified, the Agent should use `ltp-rapidx-trading`.

Trading skill responsibilities:

1. Choose MCP or CLI based on the config result.
2. Read runtime schemas before constructing write inputs.
3. Normalize symbols.
4. Query current state before trading.
5. Preview before every write.
6. Use automation sessions only after explicit user authorization.
7. Read back final order, position, transaction, or algo state.

## 3. Credentials And API Host

Required values:

```text
LTP_ACCESS_KEY
LTP_SECRET_KEY
LTP_API_HOST
```

`LTP_API_HOST` has no default. Use the API host provided by the event, environment, or workspace owner.

Best practice for non-programmer users:

1. Prefer the Agent host's user-provided chat secret mechanism.
2. Ask the user to create secrets named exactly `LTP_ACCESS_KEY`, `LTP_SECRET_KEY`, and `LTP_API_HOST`.
3. Do not ask the user to paste full keys into public chats, screenshots, logs, or repositories.

Fallbacks:

- MCP config environment references.
- Shell environment variables.
- A secret manager configured by the workspace owner.

Do not use legacy names:

```text
LTP_BASE_URL
RAPIDX_BASE_URL
RAPIDX_PORTFOLIO_ACCESS_KEY
RAPIDX_PORTFOLIO_SECRET_KEY
```

## 4. CLI Installation

Install from official npm:

```bash
npm install -g @liquiditytech/rapidx-cli@latest
```

Verify:

```bash
rapidx --version
rapidx schema --json
rapidx auth check --json
rapidx update check --json
```

For CLI-only Agents, use JSON output:

```bash
rapidx self-check --json
```

Avoid:

- wrapper scripts
- temporary JavaScript bridge files
- `cd ... && rapidx ...`
- command chains that may trigger Agent host exec preflight blocking

If the Agent host needs a working directory, configure it through the host tool setting rather than a shell chain.

## 5. MCP Configuration

MCP-capable hosts should configure the server command as:

```bash
rapidx mcp serve
```

Example MCP config:

```json
{
  "mcpServers": {
    "rapidx": {
      "command": "rapidx",
      "args": ["mcp", "serve"],
      "env": {
        "LTP_ACCESS_KEY": "<secret-ref>",
        "LTP_SECRET_KEY": "<secret-ref>",
        "LTP_API_HOST": "<secret-ref>"
      }
    }
  }
}
```

After configuration, reload or restart the MCP host and verify:

```text
rapidx/tools
rapidx/self-check
rapidx/update/check
```

Expected tool surface should include:

```text
rapidx/tools
rapidx/self-check
rapidx/update/check
rapidx/order/place-preview
rapidx/order/place
rapidx/order/replace-preview
rapidx/order/replace
rapidx/order/cancel-preview
rapidx/order/cancel
rapidx/transaction/executions
rapidx/automation/start
rapidx/automation/status
```

If old tools such as `rapidx/order/preview` or `rapidx/order/executions` appear, upgrade the CLI, restart MCP, and rerun self-check.

## 6. Version And Upgrade

Run update checks during setup, review, or session startup:

```bash
rapidx update check --json
```

Do not run network update checks before every trade. It slows execution and creates avoidable failure points.

Upgrade order:

1. Upgrade skills when the local skill version is missing, stale, or unknown.
2. Upgrade CLI.
3. Restart or reload the MCP host.
4. Run self-check again.

Skills should include a `version:` field in `SKILL.md` frontmatter. Agents should use it when comparing local skills with the release manifest.

## 7. Runtime Selection

The Agent should decide from evidence, not guessing.

| State | Meaning | Action |
|---|---|---|
| `MCP_READY` | MCP tools are visible and self-check passed. | Use MCP tools. |
| `CLI_ONLY_READY` | CLI works but MCP is unavailable. | Use CLI commands with `--json`. |
| `NOT_VERIFIED` | Runtime cannot prove tool availability. | Stop and run config self-check. |

Do not switch from MCP to CLI inside the same trade unless MCP is confirmed degraded and state has been read back.

Preview ids are runtime-local:

- MCP preview ids must be submitted through the same MCP runtime.
- CLI preview ids must be submitted through the same CLI runtime.

## 8. Session Startup Checklist

At the start of a trading session, the Agent should run:

```text
update check
self-check
portfolio overview
portfolio assets
order open-orders
position query
algo open-orders
```

MCP path:

```text
rapidx/update/check
rapidx/self-check
rapidx/portfolio/overview
rapidx/portfolio/assets
rapidx/order/open-orders
rapidx/position/query
rapidx/algo/open-orders
```

CLI path:

```bash
rapidx update check --json
rapidx self-check --json
rapidx portfolio overview --json
rapidx portfolio assets --json
rapidx order open-orders --json
rapidx position query --json
rapidx algo open-orders --json
```

## 9. Symbol And Quantity

RapidX order inputs use RapidX canonical symbols.

Recommended format:

```text
BINANCE_PERP_<BASE>_<QUOTE>
OKX_PERP_<BASE>_<QUOTE>
```

Examples:

```text
BINANCE_PERP_BTC_USDT
BINANCE_PERP_ETH_USDT
OKX_PERP_BTC_USDT
```

Normalize common user expressions:

| User expression | RapidX symbol |
|---|---|
| `BTCUSDT` | `BINANCE_PERP_BTC_USDT` |
| `btcusdt` | `BINANCE_PERP_BTC_USDT` |
| `BTC/USDT` | `BINANCE_PERP_BTC_USDT` |
| `币安人生USDT` | `BINANCE_PERP_币安人生_USDT` |

For RapidX PERP order placement:

- Use `quantity`.
- Do not send quote `amount`.
- Use `maxNotional` as a safety upper bound, not as the target order amount.

Before trading, query symbol rules:

```bash
rapidx market get-symbol-info --input '{"symbol":"BINANCE_PERP_BTC_USDT"}' --json
```

The Agent should check minimum notional, minimum quantity, lot size, price tick size, and contract size. If the requested order is below the minimum, ask the user to approve the revised quantity or notional first.

## 10. Read Before Write

Before any write, read the current state.

| Workflow | Required reads |
|---|---|
| Place order | symbol info, ticker/orderbook, portfolio assets, open orders, positions |
| Replace order | order query, open orders, symbol info |
| Cancel order | order query or open orders |
| Close position | position query, open orders |
| Algo / TPSL | position query, algo open-orders, symbol info |
| Set leverage | current leverage, position query |

The Agent should not infer current state from memory or previous chat.

## 11. Preview Then Submit

Every write with `previewRequired=true` must use:

```text
preview
→ submit with same business params + previewId + continueConsentId
→ readback
```

Order place:

```text
rapidx/order/place-preview
rapidx/order/place
rapidx/order/query
```

Order replace:

```text
rapidx/order/replace-preview
rapidx/order/replace
rapidx/order/query
```

Order cancel:

```text
rapidx/order/cancel-preview
rapidx/order/cancel
rapidx/order/query
```

Non-order writes:

```text
rapidx/trade/preview
target write tool
matching readback tool
```

If any business parameter changes after preview, create a new preview. Business parameters include symbol, side, positionSide, quantity, price, orderType, orderId, clientOrderId, leverage, and account mode.

## 12. Automation

Automation is a bounded local authorization session. It lets the Agent submit matching previews without asking for another per-order chat confirmation.

Automation still requires preview.

User authorization must include:

- symbols
- maxNotionalPerOrder
- maxTotalNotional
- duration
- allowedActions
- allowedOrderTypes
- explicit risk text

Create a session:

```bash
rapidx automation start --input '{
  "symbols": ["BINANCE_PERP_BTC_USDT"],
  "maxNotionalPerOrder": "100",
  "maxTotalNotional": "1000",
  "expiresInSeconds": 3600,
  "allowedActions": ["order.place", "order.replace", "order.cancel"],
  "allowedOrderTypes": ["MARKET", "LIMIT"],
  "explicitUserConsent": true,
  "acceptedRiskText": "I authorize RapidX automation for BINANCE_PERP_BTC_USDT with maxNotionalPerOrder 100 and maxTotalNotional 1000."
}' --json
```

Use the session in preview:

```bash
rapidx order place-preview --input '{
  "automationSessionId": "ras_xxx",
  "symbol": "BINANCE_PERP_BTC_USDT",
  "side": "BUY",
  "orderType": "MARKET",
  "quantity": "0.001",
  "maxNotional": "100",
  "clientOrderId": "auto-001"
}' --json
```

Auto-submit only when preview returns:

```json
{
  "automationSession": {
    "confirmationMode": "automation-session"
  },
  "confirmation": {
    "submitToken": "confirm_rpv_xxx"
  }
}
```

Automation management:

| Tool | Best Practice |
|---|---|
| `automation status` | Check remaining scope, expiry, and allowed actions. |
| `automation extend` | Requires new user authorization; only extends time. |
| `automation stop` | Stops future automation preview/submit; does not cancel existing orders. |

Use `allowedActions=["order.place","order.replace","order.cancel"]` for normal order lifecycle automation.

## 13. Order Types

Use runtime schema as the source of truth.

| Order type | Use when | Required fields |
|---|---|---|
| `LIMIT` | User requires price boundary. | `price`, `quantity` |
| `MARKET` | User wants immediate execution and accepts slippage. | `quantity`, `maxNotional` |

Do not silently convert a requested `MARKET` order into a best-bid or best-ask `LIMIT` order.

`MARKET` orders are supported after preview and explicit authorization. After submit, read back order status, executions, and position.

## 14. Readback And Reconciliation

Submit success is not enough. The Agent must verify final state.

After place:

```text
order query
transaction executions
position query
```

After cancel:

```text
order query until terminal
order open-orders
```

After close position:

```text
position query
transaction executions
```

After algo place:

```text
algo open-orders
algo query
```

`order.cancel` is asynchronous. `cancelAccepted=true` means the request was accepted. If `terminalStateConfirmed=false`, poll `order query` until `CANCELED`, `REJECTED`, `EXPIRED`, or timeout.

If a write times out or state is uncertain, query state before retrying. Do not blindly repeat write requests.

## 15. Position And Algo

Position close:

- Query current position first.
- NET mode: omit `positionSide`.
- HEDGE mode: use actual `LONG` or `SHORT`.
- Do not pass `side` or `quantity`.
- Use reduce-only order flow for partial close.

Set leverage:

- Preview with `targetCapabilityId="position.set-leverage"`.
- User must authorize symbol and leverage.
- Read back with `position get-leverage`.

TPSL / conditional algo:

- Preview with `targetCapabilityId="algo.place"`.
- Submit `algo place`.
- Read back with `algo open-orders` or `algo query`.
- `conditionType="ENTIRE_CLOSE_POSITION"` may use `orderType="MARKET"` without `quantity`.
- Require at least one take-profit or stop-loss trigger.

## 16. Error Handling

| status | Agent action |
|---|---|
| `INVALID_INPUT` | Fix input; do not retry unchanged. |
| `BLOCKED` | Read blocking reason; usually re-preview or ask user. |
| `NOT_FOUND` | Read current state; target may not exist or may no longer be open. |
| `PERMISSION_SCOPE_ERROR` | Credential scope does not cover the requested capability. |
| `BUSINESS_ERROR` | Upstream rule rejected the request; inspect `details`. |
| `NOT_VERIFIED` | State could not be proven; query again or report unverified. |
| `FAIL` | Diagnose auth, network, startup, or malformed response. |

Common cases:

- Invalid `orderId` format returns local `INVALID_INPUT`.
- Valid-format but missing order returns readback `NOT_FOUND`.
- Expired preview requires a new preview.
- Submit params changed after preview returns `BLOCKED`.
- Old MCP tool list means upgrade CLI and reload MCP host.

## 17. Final Answer Format

Agent final answers should include:

```text
Runtime path: MCP_READY or CLI_ONLY_READY
Tools or commands called
Symbol / side / orderType / quantity / price
Preview result
Submit result
Order id or client order id
Readback result
Final state: open, filled, cancelled, closed, unchanged, or not verified
Remaining user authorization needed, if any
```

For automation:

```text
automationSessionId
symbols
maxNotionalPerOrder
maxTotalNotional
used or remaining scope
expiresAt
allowedActions
allowedOrderTypes
```

## 18. Things Agents Must Not Do

- Do not fake query, trade, self-check, or readback results.
- Do not echo full keys.
- Do not submit writes without a preview token.
- Do not cross-submit MCP preview ids through CLI, or CLI preview ids through MCP.
- Do not shell through temporary scripts.
- Do not use `cd ... && rapidx ...` command chains.
- Do not blindly retry after timeout.
- Do not treat `maxNotional` as target order amount.
- Do not auto-increase orders to meet minimum notional without user approval.
- Do not silently replace MARKET with LIMIT.
- Do not interpret `open-orders` as "open a new order".

## 19. Minimal Safe Workflows

### First-Time Setup

```text
1. Install ltp-rapidx-config and ltp-rapidx-trading skills
2. Load and follow the installed `ltp-rapidx-config` skill
3. Install CLI from official npm
4. Configure LTP_ACCESS_KEY, LTP_SECRET_KEY, LTP_API_HOST
5. Configure MCP if supported
6. Run update check and self-check
7. Confirm MCP_READY or CLI_ONLY_READY
```

### Manual Trade

```text
1. Read portfolio, open orders, positions
2. Read symbol info and market data
3. order place-preview
4. Ask user to confirm exact preview
5. order place
6. order query
7. transaction executions or position query
```

### Automation Trade

```text
1. User authorizes automation scope in chat
2. automation start
3. order place-preview with automationSessionId
4. order place with previewId and continueConsentId
5. order query
6. automation status
```

### Replace Or Cancel

```text
1. order open-orders
2. order query
3. replace-preview or cancel-preview
4. replace or cancel
5. order query until final or known current state
```

### Close Position

```text
1. position query
2. trade preview with targetCapabilityId="position.close"
3. position close
4. position query
5. transaction executions when needed
```

### TPSL / Algo

```text
1. position query
2. algo open-orders
3. trade preview with targetCapabilityId="algo.place"
4. algo place
5. algo open-orders or algo query
```

## 20. Local Skill References

Use these local references from the installed skill directory:

- `references/best-practices.md`
- `references/capability-overview.md`
