# PolySports Skills API

## Prerequisite

- Use the host explicitly provided by the user or runtime for the current session.
- If the user specifies a test, staging, or local host, use that host for every request in this session.
- If no host is specified, use the production API host `https://api.polysports.vip`.
- Do not use `https://polysports.vip` as the API host for `/skills/v1/*`. That domain is the website and should only be used when directing the user to sign in or create an API key.
- The runtime must provide a valid `X-PolySports-Api-Key`.
- If the API key is missing, first ask the user to send their PolySports API key directly in the conversation so it can be used for this skill session.
- If the user does not have an API key yet, instruct them to register or sign in at `https://polysports.vip`, open the account menu, create an API key, and then send it back in the conversation.

## Headers

- `X-PolySports-Api-Key`: required for skill calls authenticated by API key
- `X-PolySports-Skill`: set to `polysports-trading-agent`
- `X-PolySports-Client`: caller name such as `chatgpt`
- `X-PolySports-Conversation-Id`: conversation identifier when available
- `X-Idempotency-Key`: required for write requests

## User-Facing Confirmation Rule

Do not show raw request JSON to the user. Before the first authorization or any real trade, summarize the action in plain language:

- exact game or match
- side to buy or sell
- amount or shares
- estimated execution price
- exit intent if it is already part of the plan

Never infer the amount. If the user did not provide order size, ask before any real write or before enabling automation that may trade.

If the user explicitly delegates full or discretionary trading authority, such as saying AI can trade without per-order confirmation, treat that instruction as valid approval for the `persistent` workflow. In that mode, keep showing plain-language summaries, but do not require a separate "confirm this order" turn before each in-scope trade.

## Read Endpoints

- `GET /skills/v1/me`
- `GET /skills/v1/capabilities`
- `GET /skills/v1/markets`
  Use this for broad discovery requests such as "recommend tradable NBA games" or "what can I buy today". The list response is not the final recommendation payload by itself.
- `GET /skills/v1/markets/{market_id}`
  Preferred single-detail call after the market is resolved. Reuses the Web detail aggregation and returns bundled detail in one response. In skills mode, `predictions` returns the machine-learning-only result from `/predict/ml` and does not include the Web-side LLM analysis. The same response can still include `team_stats`, `odds_compare`, `smart_money_positions`, and `game.detail` when the current membership or points access allows it.
  Access behavior should match Web: members can receive premium detail, while non-members or users without the required unlock should see the same gated result through `access` and `errors`.
- `GET /skills/v1/markets/{market_id}/snapshot`
  Lightweight detail endpoint for low-latency scans. Returns the market, token IDs, ML-only `predictions`, and normal `access/errors`, but intentionally omits slower enrichments such as smart money, team stats, odds history, odds comparison, and game detail.
- `GET /skills/v1/trading/authorization/status`
- `GET /skills/v1/trading/balance`
  Use this when the user asks for current wallet address, wallet balances, or trading buying power. The response can include both chain balances and CLOB collateral/allowance data. If the user asks to withdraw, transfer, or deposit funds, do not attempt a write flow in skills. Tell the user to complete that action in the PolySports Web wallet interface.
- `GET /skills/v1/trading/positions`
- `GET /skills/v1/trading/history`
- `GET /skills/v1/trading/orders/{order_id}`
  Use this after `POST /skills/v1/trading/order` returns an `order_id`. Wait about 5 seconds before the first check. If the order is still `submitted` with `filled_size=0`, wait another 5 to 10 seconds and check once more before telling the user it is still pending or unfilled.

## Authorization Endpoints

- `POST /skills/v1/trading/authorization-intent`
  Use this after the user asks for AI trading and you know the exact wallet and requested scopes.

- `POST /skills/v1/trading/authorization/confirm`
  Use this after the user explicitly confirms the authorization summary in natural language or explicitly delegates discretionary trading authority in natural language. A separate extra confirmation turn is not required if the delegation is already clear.

- `POST /skills/v1/trading/authorization/revoke`
  Use this when the user wants to stop or narrow AI trading authority.

Default authorization mode is `persistent`. Supported alternatives are `single_order`, `conversation`, and `timeboxed`.

## Trading Endpoints

- `POST /skills/v1/trading/preview`
- `POST /skills/v1/trading/order`
  Use this for both BUY and SELL. Standard exit flow in this skill is `side=SELL`.
- `POST /skills/v1/trading/auto-exit`
  This endpoint exists, but do not use it in this skill's standard PolySports workflow.
- `POST /skills/v1/trading/redeem`

## Scope Mapping

- `markets:read`: market discovery and market detail
- `trade:write`: authorization, preview, and order placement
- `positions:read`: wallet balance, positions, trade history, and order status
- `auto_exit:write`: stop-loss and take-profit management
- `redeem:write`: settled position redemption

## Required Behavior

- For broad list-style recommendation requests, first call `GET /skills/v1/markets`, then call `GET /skills/v1/markets/{market_id}` for the retained candidates before recommending anything.
- The list response itself does not need to be restricted to `America/New_York` today and tomorrow. Query a wider range when the user asks for it.
- ML-only prediction cache is most reliable for markets scheduled in `America/New_York` today and tomorrow. If your recommendation depends on model output, prefer those markets first. If the user asks for a farther date range or a specific market outside that window, you can still fetch detail, but you should expect `predictions` to be missing more often.
- Keep Web-equivalent gating behavior on bundled detail: membership and points access should behave the same way they do on Web.
- Resolve ambiguity before trading.
- For wallet overview questions, prefer `GET /skills/v1/trading/balance` instead of inferring buying power from positions or past trades.
- If the user asks to withdraw, transfer, or deposit, explain that skills can read balances but those wallet actions must be done in the PolySports Web wallet interface.
- Never infer order size from memory, defaults, or previous tasks. Require the user to state or confirm it.
- Prefer preview before order placement.
- If the user explicitly delegated full or persistent AI trading authority, do not force per-order confirmation for normal in-scope trades. Still provide a plain-language summary, but execution can proceed directly.
- If the user did not delegate full authority, or the intended trade materially changes side, size, strategy, or risk beyond the delegated scope, ask for confirmation before writing.
- After a real order is submitted, check the order status within about 5 seconds using `GET /skills/v1/trading/orders/{order_id}` instead of treating `submitted` as the final outcome.
- If the first status check still shows no fill and the order is not final, wait another 5 to 10 seconds and check once more. After about 20 seconds total, report the current state to the user and offer to keep monitoring if needed.
- If a PolySports position remains open after the order, move it into active monitoring rather than treating it as fire-and-forget.
- Do not use `POST /skills/v1/trading/auto-exit` for PolySports monitoring. Exit with a normal sell order when the monitoring decision says to leave.
- Reuse the same idempotency key only for a retried copy of the same write.
- Do not proactively suggest revoking a normal persistent grant after each trade. Only talk about revocation when the user asks to stop AI trading, wants narrower permissions, or the grant state itself changed.
