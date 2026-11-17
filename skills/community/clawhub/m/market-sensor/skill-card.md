## Description:

AI-driven stock and crypto analysis assistant for managing watchlists, triggering MarketSensor multi-factor analysis, retrieving reports, and checking account quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmhu](https://clawhub.ai/user/xmhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interact with the MarketSensor Open API for watchlist management, report generation, report retrieval, and quota checks across US stocks, crypto, and China A-shares. The skill should present generated market analysis as reference material rather than direct buy or sell advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenClaw prompt hook can steer broad market-related prompts toward MarketSensor even when the user did not explicitly request this service.

Mitigation: Review the hook before installation and disable or narrow it if automatic reminders are not desired.

Risk: The skill handles a MarketSensor API key and includes shell examples where command arguments may be visible to local processes or logs.

Mitigation: Use a service-scoped API key, keep it in MARKETSENSOR_API_KEY, and avoid exposing commands or environment values in shared terminals, logs, or screenshots.

Risk: Watchlist changes and analysis requests can alter the user's MarketSensor account state or consume quota.

Mitigation: Confirm removals and analysis-triggering actions with the user before executing them.

Risk: Market reports may be mistaken for direct investment recommendations.

Mitigation: Present reports as reference analysis and avoid making buy or sell recommendations on the user's behalf.

## Reference(s):

- [MarketSensor skill page](https://clawhub.ai/xmhu/skills/market-sensor)
- [MarketSensor website](https://www.marketsensor.ai)
- [MarketSensor Open API Reference](references/api-reference.md)
- [Usage examples](references/examples.md)
- [Supported markets](references/supported-markets.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, API calls, Guidance]

**Output Format:** [Markdown responses with inline shell commands and optional JSON API responses or reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MARKETSENSOR_API_KEY and may consume MarketSensor account quota or modify the user's watchlist.]

## Skill Version(s):

1.0.0 (source: server release metadata, _meta.json, and changelog released 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
