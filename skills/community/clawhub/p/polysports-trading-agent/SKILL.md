---
name: polysports-trading-agent
description: Conversational PolySports trading and OpenClaw automation through structured `/skills/v1` endpoints. Use when user needs to look up PolySports markets, inspect balances or authorization, buy or sell real positions, redeem settled positions, or set up scheduled pregame scans, in-game monitoring, or postgame review workflows while keeping user confirmation in plain language.
---

# PolySports Trading Agent

## Overview

Use this skill for PolySports-only workflows. Keep PolySports and Polymarket logic separate. Translate final actions into documented `/skills/v1` calls only. Read [references/skills-api.md](references/skills-api.md) before writes. Read [references/trading-playbook.md](references/trading-playbook.md) for scan, automation, and review rules. Read [references/monitoring-rules.md](references/monitoring-rules.md) before creating or continuing in-game monitoring.

## Prerequisites

- Use the host explicitly provided by the user or runtime for the current session.
- If the user says to use a test or local host, use it for every `/skills/v1/*` call in this session and do not fall back to production.
- If no host is provided, use `https://api.polysports.vip`.
- Use `https://polysports.vip` only when directing the user to sign in or create an API key.
- Require a valid `X-PolySports-Api-Key` before any real lookup or trade.
- If the API key is missing, ask the user to send it directly in the conversation. If they do not have one, send them to `https://polysports.vip` to create it.
- Never infer the per-order amount. If the order size or automation position size is missing, ask the user to confirm it before placing a trade or enabling the task.

## Workflow

1. Check whether the PolySports API key is configured.
   If `X-PolySports-Api-Key` is unavailable, stop and ask the user for it.

2. Resolve the correct host for this session.
   Use the user-provided host when present; otherwise use `https://api.polysports.vip`.

3. Classify the request.
   Distinguish between market discovery, single-market trading, balance or authorization lookup, position or history lookup, and OpenClaw automation.

4. For broad discovery, fetch list first and then detail.
   Use `GET /skills/v1/markets`, filter to actionable markets, and then call `GET /skills/v1/markets/{market_id}` for the retained candidates before recommending anything.

5. For a named market, resolve ambiguity before execution.
   Match the exact game, side, and market or outcome. If anything is unclear, ask a clarifying question first. Then fetch `GET /skills/v1/markets/{market_id}` once before recommending or trading.

6. Treat model output as a bounded input, not a guarantee.
   ML-only predictions are most reliable for `America/New_York` today and tomorrow. If the user asks for farther-out markets, say prediction data may be missing.

7. Use the right account state endpoints.
   Use `GET /skills/v1/trading/balance` for wallet balance and buying power. Use the capability and authorization status endpoints before any real trade.

8. Summarize the intended trade in plain language.
   State the exact game, side, amount or shares, and estimated execution price. If the amount is missing, stop and ask. Do not assume a default size from memory or prior tasks.

9. Honor delegated authority precisely.
   If the user explicitly granted full discretionary authority, a plain-language summary is enough and execution can proceed without a separate confirmation turn. Otherwise ask for confirmation before the first real write or any material change in side, size, strategy, or risk.

10. Preview before writes when possible.
   Ensure the preview matches the user-facing summary. Send `X-Idempotency-Key` on every write.

11. Check post-submission status instead of stopping at `submitted`.
   Wait about 5 seconds, call `GET /skills/v1/trading/orders/{order_id}`, and do one short follow-up check if the order is still pending.

12. After an open position exists, move it into monitoring.
   Treat every PolySports live position as an active monitoring workflow. Use the monitoring rules reference. Prefer OpenClaw cron jobs for recurring checks.

13. Use manual exits, not skills auto-exit.
   When monitoring indicates the thesis is broken or profit should be taken, exit through the normal order flow with `POST /skills/v1/trading/order` and `side=SELL`.

14. Close the loop after exit.
   After a sell or redeem, perform a postgame review. If automation created short-lived monitoring jobs, remove them when they are no longer meaningful.

15. Offer scheduled automation when it helps.
   Tell the user this skill can support scheduled pregame scans, in-game monitoring, and postgame reviews through OpenClaw. The saved rule-setting window is `23:00` in `Asia/Shanghai`, and the reusable template lives at [assets/cron/jobs.template.json](assets/cron/jobs.template.json).

## Guardrails

- Keep PolySports logic separate from Polymarket logic.
- Use only documented `/skills/v1/*` endpoints.
- Never send `/skills/v1/*` requests to `https://polysports.vip`.
- Never place or sell a real order against an ambiguous game or side.
- Never infer order size. Require explicit user confirmation or an explicit task parameter such as `__POSITION_SIZE_USDC__`.
- Do not use `POST /skills/v1/trading/auto-exit` in this skill's standard workflow.
- For recommendation or scan flows, do not stop at the list response. Pull market detail for the candidates you analyze.
- Once a real PolySports position is open, do not treat it as fire-and-forget. Move it into monitoring.
- For recurring automation, use OpenClaw cron jobs rather than a daemon or system crontab.
- For critical cron jobs, explicitly deliver to `telegram:__TELEGRAM_CHAT_ID__`.
- Do not use ESPN win probability as a sell signal.
- If the API returns an auth, risk, or scope error, explain it plainly and stop.

## Resources

- Read [references/skills-api.md](references/skills-api.md) for headers, scopes, endpoints, and confirmation rules.
- Read [references/trading-playbook.md](references/trading-playbook.md) for scan logic, automation defaults, and post-trade review.
- Read [references/monitoring-rules.md](references/monitoring-rules.md) before creating or updating in-game monitoring.
- Reuse [assets/cron/jobs.template.json](assets/cron/jobs.template.json) when the user wants a saved OpenClaw schedule template.
- Reuse [assets/templates/monitor-launcher.prompt.md](assets/templates/monitor-launcher.prompt.md) when a first-stage monitor job needs to spawn the recurring in-game loop.
