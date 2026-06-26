# PolySports Trading Playbook

## Scope

- Keep PolySports and Polymarket separated.
- Treat PolySports as pregame selection plus active in-game management, not passive buy-and-wait settlement.

## Order Sizing

- Do not keep or apply a default unit size inside the skill.
- Before any real buy order, or any automation that may buy, confirm the per-order USDC amount with the user.
- Fill `__POSITION_SIZE_USDC__` explicitly in templates before use.
- If the user changes risk tolerance or wants different sizing rules, restate the sizing rule back before enabling automation.

## Discovery and Scan

- For scheduled daily scans, default focus is NBA unless the user says otherwise.
- Always call the market list first and then pull detail for shortlisted markets.
- Base the decision on bundled detail: current price, ML prediction if available, `odds_compare`, smart money or holder signals when available, recent team form, injuries, rotation context, and targeted web search when needed.
- Prefer no trade over weak edge.
- Avoid duplicate direction if the same market or outcome is already held or already traded that day.

## Automation

- Prefer OpenClaw cron jobs, not long-running scripts or system crontab.
- Supported scheduled workflows are:
  - Pregame scan
  - In-game monitoring
  - Postgame review
- The default rule-setting or refresh window is `23:00` in `Asia/Shanghai`.
- Reuse [../assets/cron/jobs.template.json](../assets/cron/jobs.template.json) as the saved template for daily scans.
- Reuse [../assets/templates/monitor-launcher.prompt.md](../assets/templates/monitor-launcher.prompt.md) when a first-stage monitor needs to create the recurring in-game loop.
- Fill placeholders such as `__POLYSPORTS_API_KEY__`, `__TELEGRAM_CHAT_ID__`, and `__POSITION_SIZE_USDC__` before enabling a job.
- Send critical jobs to `telegram:__TELEGRAM_CHAT_ID__`.
- Every automated run must report an outcome, including "no trade" and execution failure.

## Exit and Review

- Do not use skills auto-exit for PolySports.
- Exit through `POST /skills/v1/trading/order` with `side=SELL`.
- After a position is closed or redeemed, do a postgame review regardless of profit or loss.
- Delete short-lived monitoring tasks once they no longer matter or after a successful exit.
