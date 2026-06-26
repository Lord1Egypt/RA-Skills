---
name: ltp-rapidx-config
version: 1.0.14
description: Use when an agent needs to install or configure RapidX CLI/MCP access, set production LTP credentials, locate the agent workspace MCP config, review integration, discover tools, or run read-only self-checks.
---

# RapidX Config

Use this skill for setup and integration review only. Use `ltp-rapidx-trading` for portfolio, market, order, position, algo, and live trading workflows.

## Scope

- Configure the published RapidX CLI package as the single runtime entrypoint.
- Configure MCP by launching `rapidx mcp serve` from the agent's own workspace MCP config.
- Classify whether this agent host is `MCP_READY`, `CLI_ONLY_READY`, or `NOT_VERIFIED`.
- Verify real tool availability with read-only calls.
- Produce an integration review with masked credentials and actual evidence.

Do not describe how to install this skill inside the skill itself. Assume the skill has already been installed by the agent host.

## References

- Read `references/capability-overview.md` when checking expected CLI commands, MCP tools, capability names, or endpoint coverage.
- Read `references/best-practices.md` when doing a full RapidX Skills / CLI / MCP setup review or explaining the recommended external user flow.

## Workspace First

Before changing MCP config, identify the agent host workspace that will run RapidX:

1. State the active agent workspace path from session/runtime context.
2. Identify the workspace-local MCP config file read by this same agent host.
3. If the MCP config path is ambiguous, inspect the confirmed workspace for existing MCP settings.
4. If still ambiguous, ask the user which MCP config file this agent should edit.
5. Add or update `mcpServers.rapidx` only after the workspace and config path are known.

Never assume the source repository root, filesystem root, or a global home config is the right target.

## Credential Intake

Ask whether the user wants to provide credentials as a user-provided chat secret. This is the default path for non-programmers, but state the risk first: even protected chat-secret flows are controlled by the agent host and may be subject to that host's retention, access, or collaboration settings.

If the agent host has a dedicated chat-secret UI, ask the user to create three secrets with the exact names `LTP_ACCESS_KEY`, `LTP_SECRET_KEY`, and `LTP_API_HOST`. If the host has no chat-secret UI, ask whether the user wants the agent to write masked-reference placeholders into MCP config or whether they prefer to set local environment variables manually.

Offer alternatives when the user wants stronger isolation:

- Local shell environment variables.
- Enterprise or OS secret manager referenced by the MCP host.

Rules:

- Required variables are `LTP_ACCESS_KEY`, `LTP_SECRET_KEY`, and `LTP_API_HOST`.
- `LTP_API_HOST` has no default. Use the API host provided for the current environment.
- Do not use `LTP_BASE_URL`, `RAPIDX_BASE_URL`, or `RAPIDX_PORTFOLIO_*`.
- Do not ask for or echo complete keys in normal chat text when a chat-secret mechanism is available.
- Never print full keys in logs, config review, test output, or evidence. Use masked values only.

## CLI Install

RapidX is published as an official npm package. Install the CLI:

```bash
npm install -g @liquiditytech/rapidx-cli
```

If global install is not allowed, install in the confirmed agent workspace and use the workspace-local executable path in MCP config:

```bash
npm install @liquiditytech/rapidx-cli
./node_modules/.bin/rapidx --version
```

Verify the installed CLI:

```bash
rapidx --version
rapidx schema --json
rapidx update check --json
rapidx self-check --json
```

`rapidx schema --json` and MCP `rapidx/tools` must return both `capabilities`/tool entries and concrete `inputSchemas`.

For CLI-only agents, use direct `rapidx ... --json` commands. Do not create temporary bridge scripts, directory-changing shell chains, or shell command chaining for MCP access.

## Upgrade Existing Installation

Use the CLI as the single version-check entrypoint. If `rapidx` is already available, run:

```bash
rapidx update check --json
```

Read these fields:

- CLI: `currentVersion`, `latestVersion`, `status`, `updateAvailable`, `writeAllowed`, `upgrade.global`, `upgrade.workspace`.
- Skills: `skillsVersion`, `currentSkillsVersion`, `skillsUpdateRecommended`, `upgrade.skills`.

`currentSkillsVersion` is the CLI-bundled expected skills version, not proof of the agent's installed local skills. Inspect the installed or loaded `ltp-rapidx-config` and `ltp-rapidx-trading` frontmatter. Each current skill must declare `version`. When the local version is known, pass it into the check:

```bash
rapidx update check --input '{"installedSkillsVersion":"<local-skill-version>"}' --json
```

For upgrade review, force a remote manifest refresh:

```bash
rapidx update check --input '{"installedSkillsVersion":"<local-skill-version>","force":true}' --json
```

Compare the local `version` with `latestSkillsVersion` or legacy `skillsVersion` from `rapidx update check --json`. If the local version is missing, lower than the latest skills version, or cannot be read, update or reinstall both RapidX skills using the agent host's normal skill installer, then restart or reload the agent so the new skill content is loaded.

Upgrade order:

1. Update or reinstall both RapidX skills if their local `version` is stale, missing, or unknown.
2. Restart or reload the agent so the new skills are active.
3. Upgrade CLI when `updateAvailable=true`, `status=UPGRADE_REQUIRED`, or `status=WRITE_BLOCKED`.
4. Restart or reload the MCP host when MCP is configured.
5. Run `rapidx --version`, `rapidx update check --json`, and `rapidx self-check --json`.
6. If MCP is supported, verify `rapidx/tools`, `rapidx/update/check`, and `rapidx/self-check`.

Official npm CLI upgrade:

```bash
npm install -g @liquiditytech/rapidx-cli@latest
```

Workspace-local CLI upgrade:

```bash
npm install @liquiditytech/rapidx-cli@latest
./node_modules/.bin/rapidx --version
```

## Runtime Path Selection

Classify the agent after CLI install and, when available, MCP configuration. Do not classify from agent product name or config file existence alone.

Before install, only choose a candidate path:

- If the host exposes workspace MCP config plus native tool discovery/call surfaces, attempt the MCP path.
- If the host only exposes shell, exec, or terminal commands, use the CLI-only path.
- If uncertain, install CLI first, run CLI self-check, and keep MCP as `NOT_VERIFIED` until MCP tools are actually callable.

After install/config, set one status:

- `CLI_READY`: `rapidx --version` and `rapidx schema --json` pass.
- `MCP_READY`: `CLI_READY`, `initialize` returns `serverInfo.name=rapidx`, `tools/list` shows 46 `rapidx/...` tools, and `rapidx/tools`, `rapidx/update/check`, plus `rapidx/self-check` can be called as MCP tools.
- `CLI_ONLY_READY`: `CLI_READY`, but the host cannot configure, discover, or call MCP tools.
- `NOT_VERIFIED`: no real invocation evidence, or only a config file was edited.

Writing `mcpServers.rapidx` is only an attempted MCP setup. It is not proof of MCP readiness. If MCP is not `MCP_READY`, mark MCP as `NOT_VERIFIED` and use direct `rapidx ... --json` commands.

## MCP Config

MCP is started by the CLI. Add this server to the agent workspace MCP config:

```json
{
  "mcpServers": {
    "rapidx": {
      "command": "rapidx",
      "args": ["mcp", "serve"],
      "env": {
        "LTP_ACCESS_KEY": "<user-provided-secret-or-env-reference>",
        "LTP_SECRET_KEY": "<user-provided-secret-or-env-reference>",
        "LTP_API_HOST": "<user-provided-secret-or-env-reference>"
      }
    }
  }
}
```

The MCP server command should be `rapidx` with args `["mcp", "serve"]` when `rapidx` is on the MCP host PATH. If PATH is not guaranteed, use the absolute path to the installed `rapidx` executable as `command` and keep args as `["mcp", "serve"]`. Do not point MCP tools at one-off CLI commands and do not add shell script wrappers.

Host-specific setup examples:

```text
Codex:
  codex mcp add rapidx -- rapidx mcp serve

Claude Code:
  claude mcp add --transport stdio rapidx -- rapidx mcp serve

Cursor:
  Add to mcp.json:
  {"mcpServers":{"rapidx":{"command":"rapidx","args":["mcp","serve"],"env":{"LTP_ACCESS_KEY":"<secret>","LTP_SECRET_KEY":"<secret>","LTP_API_HOST":"<secret>"}}}}

Gemini CLI:
  gemini mcp add rapidx rapidx -- mcp serve

OpenCode:
  Add to opencode.jsonc:
  {"mcp":{"rapidx":{"type":"local","command":["rapidx","mcp","serve"],"enabled":true}}}

OpenClaw:
  openclaw mcp add rapidx --command rapidx --arg mcp --arg serve
  openclaw mcp doctor rapidx --probe

Hermes:
  hermes mcp add rapidx --command rapidx --args mcp serve
```

For OpenClaw, use repeated `--arg` entries. Do not use `--args`.

For Hermes, use a single `--args` and put `mcp serve` after it. Do not repeat `--args`, because Hermes treats the first `--args` as the start of the child command arguments.

If a host CLI tries to run an interactive `mcp add` flow and blocks on prompts like enabling all tools, do not keep retrying it in a non-interactive terminal. Edit the confirmed workspace MCP config directly with the JSON above, then restart or reload the agent host and verify through real MCP tool discovery.

## Expected MCP Tools

Healthy MCP discovery exposes 46 tools:

```text
Discovery: rapidx/tools, rapidx/self-check, rapidx/update/check
Market:    rapidx/market/get-ticker, rapidx/market/get-orderbook, rapidx/market/get-klines,
           rapidx/market/get-funding-rate, rapidx/market/get-mark-price,
           rapidx/market/get-symbol-info, rapidx/market/get-open-interest
Portfolio: rapidx/portfolio/overview, rapidx/portfolio/assets,
           rapidx/portfolio/statement, rapidx/portfolio/user-fee-rate,
           rapidx/portfolio/position-bracket, rapidx/portfolio/set-position-mode
Trade:     rapidx/trade/preview, rapidx/trade/verify-live
Automation:
           rapidx/automation/start, rapidx/automation/list,
           rapidx/automation/status, rapidx/automation/extend,
           rapidx/automation/stop
Order:     rapidx/order/place-preview, rapidx/order/replace-preview,
           rapidx/order/cancel-preview,
           rapidx/order/place, rapidx/order/replace, rapidx/order/cancel,
           rapidx/order/cancel-all, rapidx/order/query,
           rapidx/order/open-orders, rapidx/order/history
Transactions:
           rapidx/transaction/executions
Position:  rapidx/position/query, rapidx/position/history,
           rapidx/position/get-leverage, rapidx/position/close,
           rapidx/position/close-all, rapidx/position/set-leverage
Algo:      rapidx/algo/place, rapidx/algo/replace, rapidx/algo/cancel,
           rapidx/algo/open-orders, rapidx/algo/history, rapidx/algo/query
```

`open-orders` means current non-terminal orders, not "open an order". These orders may still be fillable, replaceable, or cancelable. `algo/open-orders` means current non-terminal algo orders such as conditional or TPSL orders that have not triggered, been canceled, or otherwise ended.

Legacy snake_case names such as `get_ticker`, `place_order`, or `list_positions` indicate a stale integration and should not be used.

## Read-Only Self-Check

The self-check proves the configured runtime is real. Do not simulate results, invent balances, or claim success from documentation alone.

Run the quick check:

1. Confirm `CLI_READY` with `rapidx --version` and `rapidx schema --json`, including readable `inputSchemas`.
2. Run `rapidx update check --json` during setup or review. This may read the GitHub release manifest and cache the result locally.
3. If attempting MCP, discover tools through the MCP host and confirm the 46-tool inventory.
4. Call `rapidx/update/check` when the host supports MCP tool invocation.
5. Call `rapidx/self-check` when the host supports MCP tool invocation.
6. Call one public market route, preferably `rapidx/market/get-ticker` for `BINANCE_PERP_BTC_USDT`. If the user provides a Binance native symbol, normalize it before calling RapidX: `BTCUSDT` becomes `BINANCE_PERP_BTC_USDT`, and a Chinese base asset such as `币安人生USDT` becomes `BINANCE_PERP_币安人生_USDT`.
7. Call read routes for portfolio overview, portfolio assets, open orders, positions, and algo orders.

If the host cannot invoke MCP tools yet, run equivalent CLI read-only checks and mark MCP tool invocation as `NOT_VERIFIED`; do not convert CLI success into MCP success.

Run the deeper review when asked for integration review or self-validation:

```text
1. rapidx/tools
2. rapidx/update/check
3. rapidx/self-check
4. rapidx/market/get-ticker
5. rapidx/market/get-orderbook
6. rapidx/market/get-klines
7. rapidx/market/get-funding-rate
8. rapidx/market/get-mark-price
9. rapidx/market/get-symbol-info
10. rapidx/market/get-open-interest
11. rapidx/portfolio/overview
12. rapidx/portfolio/assets
13. rapidx/order/open-orders
14. rapidx/order/history
15. rapidx/order/query with a deliberately nonexistent self-check order id
16. rapidx/position/query
17. rapidx/position/history
18. rapidx/algo/open-orders
19. rapidx/algo/history
20. rapidx/algo/query with a deliberately nonexistent self-check algo order id
```

Do not call removed `mode="account"` portfolio asset checks during setup. `rapidx/portfolio/assets` is the supported balance/assets read for portfolio credentials.

## Result Classes

- `PASS`: actual tool or command returned a successful real response.
- `EXPECTED_ERROR`: route is live and returned a real business, permission, unsupported-mode, or deliberate not-found error.
- `INVALID_INPUT`: schema or local input validation rejected the request before submission.
- `NOT_FOUND`: a syntactically valid requested resource does not exist, such as a valid-format order id that RapidX cannot find.
- `PERMISSION_SCOPE_ERROR`: credentials are valid but do not cover the requested route or portfolio scope.
- `BUSINESS_ERROR`: RapidX or the venue returned a business-rule rejection.
- `FAIL`: tool is missing, startup/auth/network failed, response is malformed, or a required call timed out.
- `NOT_VERIFIED`: the agent could not invoke the tool or the user declined credentials.

If update check returns `WRITE_BLOCKED`, `UPGRADE_REQUIRED`, or `skillsUpdateRecommended=true`, report it in the review. Do not run trading writes until a `WRITE_BLOCKED` or `UPGRADE_REQUIRED` CLI is upgraded and the MCP host is restarted.

Every row must include `toolOrCommandEvidence` or equivalent observed code/message evidence. Empty order, position, or history lists are `PASS` if the response is real and well formed.

## Integration Review Output

Return this structure when asked to review setup:

```markdown
# RapidX Integration Review

## Verdict
- status: PASS / PARTIAL / FAIL / NOT_VERIFIED
- runtime path: MCP_READY / CLI_ONLY_READY / NOT_VERIFIED
- main issues:

## Workspace And Config
- agent workspace:
- MCP config path:
- MCP command: rapidx mcp serve
- CLI package:
- host:
- credentials: configured and masked / missing / not verified

## Tool Discovery
- expected MCP tools: 46
- actual MCP tools:
- missing tools:
- legacy tools found:

## Version And Upgrade
- current CLI:
- latest CLI:
- minimum write version:
- update status:
- skills update recommended:

## Read-Only Checks
| check | result | evidence |
| --- | --- | --- |

## Required Fixes
- ...
```

Switch to `ltp-rapidx-trading` for any write verification or live trading test.
