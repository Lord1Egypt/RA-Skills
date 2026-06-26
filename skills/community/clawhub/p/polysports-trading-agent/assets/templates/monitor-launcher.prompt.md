This is a PolySports two-stage monitor launcher template.

Read first:

- `skills/polysports-trading-agent/SKILL.md`
- `skills/polysports-trading-agent/references/skills-api.md`
- `skills/polysports-trading-agent/references/monitoring-rules.md`

Current target:

- Match: `__MATCH_LABEL__`
- Market ID: `__MARKET_ID__`
- Outcome: `__OUTCOME__`
- Token ID: `__TOKEN_ID__`
- Telegram target: `telegram:__TELEGRAM_CHAT_ID__`

Your task:

1. Immediately create the second-stage `every 5m` monitoring cron.
2. The second stage must explicitly include the correct API host, API key header rules, monitoring inputs, SELL execution rules, double-checking empty positions, self-deletion, and postgame review requirements.
3. When creating the job, include `--to telegram:__TELEGRAM_CHAT_ID__ --channel telegram --account default --announce`.
4. After creation succeeds, immediately report the second-stage cron id, next run time, and delivery target.

Once creation is complete, this launcher task can finish.
