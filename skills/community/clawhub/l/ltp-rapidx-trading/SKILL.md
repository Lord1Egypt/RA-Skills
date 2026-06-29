---
name: ltp-rapidx-trading
version: 1.0.15
description: Use when an agent needs to operate RapidX through MCP or CLI for portfolio reads, market reads, order preview, order submit/replace/cancel, position management, algo orders, or explicit live trading verification.
---

# RapidX Trading

Use this skill after `ltp-rapidx-config` has confirmed the runtime path as `MCP_READY` or `CLI_ONLY_READY`. Prefer MCP tools only when the agent host is `MCP_READY`. Use direct CLI commands only when the confirmed path is `CLI_ONLY_READY`.

## References

- Read `references/capability-overview.md` when selecting a CLI command, MCP tool, capability id, or RapidX endpoint mapping.
- Read `references/best-practices.md` when planning a full workflow across skills, CLI, MCP, preview, automation, and readback.

## Non-Negotiable Rules

- Do not fake query or trading results. Every claim must come from an actual MCP tool or `rapidx ... --json` response, and final summaries must include `toolOrCommandEvidence` or equivalent observed evidence.
- Do not use shell bridge scripts, temporary JavaScript scripts, directory-changing shell chains, or chained shell invocations.
- Treat all trade-write tools as real production actions.
- Never submit a write without preview evidence and explicit user consent for that specific write, unless the user has explicitly enabled RapidX automation mode for the current scope in chat.
- Use `confirmation.submitToken` from the preview response as the submit `continueConsentId`.
- Keep business parameters unchanged between preview and submit. If symbol, side, positionSide, quantity, price, order id, leverage, or mode changes, create a new preview.
- If a write times out or the result is uncertain, query state before retrying.
- Never echo secrets.

## Invocation Path

Before any trading workflow, read the latest integration review from `ltp-rapidx-config` or run that skill first.

- `MCP_READY`: use `rapidx/...` MCP tools and do not shell out to wrapper scripts.
- `CLI_ONLY_READY`: use direct `rapidx ... --json` commands and do not claim MCP tools were called.
- `NOT_VERIFIED` or only `CLI_READY`: stop and run config self-check before portfolio, market, or trade workflows.

Do not switch paths during a task without new evidence. If an MCP call fails after `MCP_READY`, mark MCP degraded and verify state before retrying or falling back to CLI.

If MCP setup or discovery is missing, stale, or failing, stop trading setup work and return to `ltp-rapidx-config` MCP Config. Do not invent host-specific MCP add commands in this trading skill.

## Version Check

At the start of a trading session or before the first write in a session, check the cached release status once:

- `MCP_READY`: call `rapidx/update/check` once, then `rapidx/self-check`.
- `CLI_ONLY_READY`: run `rapidx update check --json`.

Do not perform a fresh network update check before every trade submit. If the update result is `WRITE_BLOCKED`, `UPGRADE_REQUIRED`, or `skillsUpdateRecommended=true`, stop all trade-write actions and run `ltp-rapidx-config` upgrade handling first. Upgrade or reinstall skills first when their local frontmatter `version` is missing, stale, or unknown; then upgrade the CLI when needed, restart or reload the MCP host when applicable, and rerun self-check. Do not block read-only work solely because skills update is recommended.

## Current MCP Surface

Use `rapidx/tools` for the authoritative runtime schema. It returns the tool list plus concrete `inputSchemas`; read the relevant input schema before constructing write inputs. Current normal-use tool names are:

```text
Market:   rapidx/market/get-ticker, rapidx/market/get-orderbook,
          rapidx/market/get-klines, rapidx/market/get-funding-rate,
          rapidx/market/get-mark-price, rapidx/market/get-symbol-info,
          rapidx/market/get-open-interest
Portfolio: rapidx/portfolio/overview, rapidx/portfolio/assets,
          rapidx/portfolio/statement, rapidx/portfolio/user-fee-rate,
          rapidx/portfolio/position-bracket, rapidx/portfolio/set-position-mode
Update:   rapidx/update/check
Trade:    rapidx/trade/preview, rapidx/trade/verify-live
Automation:
          rapidx/automation/start, rapidx/automation/list,
          rapidx/automation/status, rapidx/automation/extend,
          rapidx/automation/stop
Order:    rapidx/order/place-preview, rapidx/order/replace-preview,
          rapidx/order/cancel-preview, rapidx/order/place,
          rapidx/order/replace, rapidx/order/cancel,
          rapidx/order/cancel-all, rapidx/order/query,
          rapidx/order/open-orders, rapidx/order/history
Transactions:
          rapidx/transaction/executions
Position: rapidx/position/query, rapidx/position/history,
          rapidx/position/get-leverage, rapidx/position/close,
          rapidx/position/close-all, rapidx/position/set-leverage
Algo:     rapidx/algo/place, rapidx/algo/replace,
          rapidx/algo/cancel, rapidx/algo/open-orders,
          rapidx/algo/history, rapidx/algo/query
```

Use `rapidx/trade/verify-live` for small real-trade verification.

`open-orders` means current non-terminal orders, not "open an order". These orders may still be fillable, replaceable, or cancelable. `algo/open-orders` means current non-terminal algo orders such as conditional or TPSL orders that have not triggered, been canceled, or otherwise ended.
`rapidx/order/history` and `rapidx/algo/history` accept optional `begin` and `end` timestamps in milliseconds; if omitted, RapidX applies the upstream server default range.

## Read Workflow

Before making trading decisions, refresh state:

```text
1. rapidx/portfolio/overview
2. rapidx/portfolio/assets
3. rapidx/order/open-orders
4. rapidx/position/query
5. rapidx/algo/open-orders
6. rapidx/transaction/executions when fills/transactions are needed
```

For a symbol, refresh market data:

```text
1. rapidx/market/get-symbol-info
2. rapidx/market/get-ticker
3. rapidx/market/get-orderbook
4. rapidx/market/get-mark-price
5. rapidx/market/get-klines
6. rapidx/market/get-funding-rate      # PERP only
7. rapidx/market/get-open-interest     # PERP only
```

Use RapidX symbol format `BINANCE_PERP_<BASE>_<QUOTE>`, for example `BINANCE_PERP_BTC_USDT` or `BINANCE_PERP_ETH_USDT`. `OKX_PERP_<BASE>_<QUOTE>` is supported for OKX perpetual instruments. If the user says an OKX swap symbol, `OKX_SWAP_<BASE>_<QUOTE>` is accepted as an input alias and normalizes to `OKX_PERP_<BASE>_<QUOTE>`. Market adapters may return `originalSymbol` for venue-native symbols such as `BTCUSDT` or `BTC-USDT-SWAP`.

Normalize user-facing Binance symbols before tool calls. If the user says `BTCUSDT`, `btcusdt`, or `BTC/USDT`, call RapidX with `BINANCE_PERP_BTC_USDT`. If the base asset contains Chinese characters, preserve the base exactly: `币安人生USDT` becomes `BINANCE_PERP_币安人生_USDT`. Do not translate Chinese base assets. Do not pass Binance native symbols directly as the `symbol` field. If exchange, type, base, or quote cannot be identified, ask the user to confirm the RapidX symbol first.

Inspect symbol info before placing or replacing orders.
For hedge-mode orders, pass `positionSide="LONG"` or `positionSide="SHORT"` in order placement, algo placement, set-leverage, or verify-live inputs when the schema exposes it. Do not call `rapidx/portfolio/set-position-mode` just to choose an order side.

## Preview Then Submit

All writes use this pattern:

1. Call the write-specific preview tool.
2. Read `previewId` and `confirmation.submitToken`.
3. Show the user the actual `requestSummary`, `businessParams`, max notional, order id/client order id, and `riskNotes`.
4. Ask for explicit consent for this one write.
5. Submit the target write with the same business parameters plus `previewId` and `continueConsentId=<confirmation.submitToken>`.
6. Query resulting state with the relevant read tool.

If the preview response does not include `confirmation.submitToken`, do not submit the write. Re-run preview with the current CLI/MCP runtime or report the integration as stale.

Preview ids are runtime-local. Use MCP preview ids only with the same MCP server runtime. Use CLI preview ids only with the same CLI preview store. Do not cross-submit MCP preview ids through CLI, or CLI preview ids through MCP.

Automation session still requires preview. Use it only when the user explicitly enables RapidX automation in chat and authorizes symbol, per-order max notional, total max notional, duration, allowed actions, and allowed order types. For normal order lifecycle automation, use `allowedActions=["order.place","order.replace","order.cancel"]`. First create a session with `rapidx/automation/start`; the input must include `explicitUserConsent=true` and `acceptedRiskText` copied from the user's authorization. Then add `automationSessionId` to order place/replace/cancel preview input. If the preview returns `automationSession.confirmationMode="automation-session"` and `confirmation.submitToken`, submit that preview without asking for another per-order chat confirmation. Do not invent automation scope. If no matching session exists, create one only after user authorization. If multiple sessions match, ask which session to use or pass the intended `automationSessionId`.

Automation session flow:

```text
1. rapidx/automation/start with explicitUserConsent=true and acceptedRiskText from the user
2. rapidx/order/place-preview, rapidx/order/replace-preview, or rapidx/order/cancel-preview with automationSessionId
3. Submit the matching order write with the same business parameters plus previewId and continueConsentId
4. rapidx/automation/status when the agent needs remaining session scope
5. rapidx/automation/extend only after the user authorizes more time; include explicitUserConsent=true and a new acceptedRiskText
6. rapidx/automation/stop when the user says to stop automation
```

Stopping automation blocks future automation previews/submits. It does not cancel existing orders.

Automation notional accounting: `order.place` consumes notional by `maxNotional`; `order.replace` consumes the replacement order notional; `order.cancel` consumes no notional.

`maxNotional` is a safety upper bound, not the target order quantity. Before increasing quantity or notional to satisfy an exchange rule, check symbol `minNotional` and ask the user to confirm the new quantity or notional.

Order placement:

```text
rapidx/order/place-preview
rapidx/order/place
rapidx/order/query or rapidx/order/open-orders
```

Order replace:

```text
rapidx/order/replace-preview
rapidx/order/replace
rapidx/order/query or rapidx/order/open-orders
```

Order cancel:

```text
rapidx/order/cancel-preview
rapidx/order/cancel
rapidx/order/open-orders
```

`rapidx/order/cancel` is asynchronous. If the result has `cancelAccepted=true` and `terminalStateConfirmed=false`, poll `rapidx/order/query` until `CANCELED`, `REJECTED`, `EXPIRED`, or timeout before claiming a final state.

Non-order writes:

```text
rapidx/trade/preview with targetCapabilityId
target tool, such as rapidx/position/set-leverage
matching read-back tool
```

Common `targetCapabilityId` values are `position.set-leverage`, `position.close`, `portfolio.set-position-mode`, `algo.place`, `algo.replace`, and `algo.cancel`.

## Order Rules

- LIMIT order: requires quantity and price.
- MARKET order: allowed after preview and explicit user authorization. Treat it as immediate execution with possible slippage and no guaranteed fill price.
- For RapidX PERP order placement, pass `quantity`. Do not use quote `amount`.
- PERP writes are leverage and margin sensitive.
- Hedge-mode order placement uses `positionSide="LONG"` or `positionSide="SHORT"` when needed.
- Use a stable `clientOrderId` when the schema accepts one so status can be checked after a timeout.
- Do not infer fills from placement. Confirm through `order/query`, `order/open-orders`, `order/history`, executions, or positions.
- If a requested order is below the symbol `minNotional`, do not auto-increase to the minimum. Ask the user to approve the revised quantity or notional first.
- Do not tell users that RapidX blocks all MARKET orders by default. Do not silently replace a requested MARKET order with a best-bid/best-ask LIMIT order.

## Algo Orders

Use preview/submit for `rapidx/algo/place`, `rapidx/algo/replace`, and `rapidx/algo/cancel`.

Before placing TPSL or conditional orders:

- Confirm target symbol, side, quantity when required, trigger price, stop/take-profit intent, and position side if hedge mode is used.
- For TPSL, require at least one valid take-profit or stop-loss trigger.
- `conditionType="ENTIRE_CLOSE_POSITION"` may use `orderType="MARKET"` without `quantity`.
- After submit, verify through `rapidx/algo/open-orders`.

## Position And Portfolio Risk Writes

Use separate explicit consent for each:

- `rapidx/position/set-leverage` changes future risk for the symbol.
- `rapidx/portfolio/set-position-mode` changes account position mode and can affect existing workflows. Use it only when the user explicitly asks to change account position mode.
- `rapidx/position/close` is a real close-position action. Verify current position first.

Do not pass `side` or `quantity` to `position.close`. The close-position API determines BUY or SELL from the current position and closes the target symbol/positionSide. In NET mode, closing a long behaves like SELL and closing a short behaves like BUY. Treat `position.close` as a market close unless the tool schema explicitly exposes another order type, and verify the result with `rapidx/position/query`. Use a reduce-only order flow for partial closes. If `order/query` later shows `reduceOnly=false`, do not treat that alone as a failed close; `position.close` uses the RapidX close-position API and the order readback may not echo the reduce-only intent.

Do not test these writes as part of ordinary setup.

## Live Trading Verification

Use `rapidx/trade/verify-live` only when the user explicitly asks for a small real-trade verification and authorizes symbol, exchange, notional cap, cleanup behavior, and test window. The tool input must include `acceptedRiskText` that names the exact symbol, side, positionSide when provided, maxNotional, real-order risk, and cancel cleanup behavior.

The verification must include:

```text
1. read-only self-check
2. market and symbol rule lookup
3. explicit user consent
4. internal preview
5. post-only or safely far-from-market limit submit
6. order query
7. replace when supported
8. cancel
9. cleanup check for open orders, positions, and algo orders
```

If any step cannot be verified, return `NOT_VERIFIED`, `EXPECTED_ERROR`, `INVALID_INPUT`, `BLOCKED`, `NOT_FOUND`, `PERMISSION_SCOPE_ERROR`, `BUSINESS_ERROR`, or `FAIL` with observed evidence. Do not call it successful without real evidence.

Order id checks have two layers: invalid `orderId` format is local `INVALID_INPUT`; valid-format but missing/non-open orders are discovered through RapidX readback during `order.query`, `order.replace-preview`, or `order.cancel-preview` and should be reported as `NOT_FOUND` or `BLOCKED` with evidence. If the user provides only `clientOrderId`, do not invent or validate an `orderId`.

## CLI Fallback

When MCP is unavailable, use direct CLI equivalents with `--json` and the same preview/submit discipline:

```bash
rapidx order place-preview --input '{"symbol":"BINANCE_PERP_BTC_USDT","side":"BUY","orderType":"LIMIT","price":"65000","quantity":"0.001","maxNotional":"100","clientOrderId":"example-001"}' --json
rapidx order place --input '{"symbol":"BINANCE_PERP_BTC_USDT","side":"BUY","orderType":"LIMIT","price":"65000","quantity":"0.001","maxNotional":"100","clientOrderId":"example-001","previewId":"<previewId>","continueConsentId":"<confirmation.submitToken>"}' --json
rapidx automation start --input '{"symbols":["BINANCE_PERP_BTC_USDT"],"maxNotionalPerOrder":"100","maxTotalNotional":"1000","expiresInSeconds":3600,"allowedActions":["order.place","order.replace","order.cancel"],"allowedOrderTypes":["MARKET","LIMIT"],"explicitUserConsent":true,"acceptedRiskText":"I authorize RapidX automation for BINANCE_PERP_BTC_USDT with maxNotionalPerOrder 100 and maxTotalNotional 1000."}' --json
rapidx order place-preview --input '{"automationSessionId":"<automationSessionId>","symbol":"BINANCE_PERP_BTC_USDT","side":"BUY","orderType":"MARKET","quantity":"0.001","maxNotional":"60","clientOrderId":"auto-001"}' --json
rapidx trade preview --input '{"targetCapabilityId":"position.set-leverage","symbol":"BINANCE_PERP_BTC_USDT","leverage":5}' --json
rapidx trade verify-live --input '{"symbol":"BINANCE_PERP_BTC_USDT","side":"BUY","maxNotional":"100","clientOrderId":"verify-001","explicitUserConsent":true,"acceptedRiskText":"I authorize a real verification order for BINANCE_PERP_BTC_USDT BUY maxNotional 100 with cancel cleanup."}' --json
```

Avoid shell chaining and wrapper scripts. Run commands from the agent workspace or use absolute paths supported by the host.

## Final Answer

For trading work, state:

- Which real tools or commands were called.
- Which portfolio/order/position facts were verified.
- Whether the final state is open, filled, cancelled, closed, unchanged, or not verified.
- Any remaining action the user must explicitly authorize.
