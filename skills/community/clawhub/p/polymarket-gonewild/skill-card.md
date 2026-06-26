## Description: <br>
Query Polymarket prediction markets, including odds, trending markets, event search, price momentum, watchlist alerts, resolution calendars, and simulated paper trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShrimpDaddie](https://clawhub.ai/user/ShrimpDaddie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect public Polymarket prediction-market data, monitor price movements, receive local watchlist alerts, and track simulated paper positions without wallet credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Polymarket's public Gamma API for market data. <br>
Mitigation: Install and run it only in environments where outbound requests to Polymarket's public API are acceptable. <br>
Risk: Watchlist entries and simulated portfolio data are stored locally under ~/.polymarket/. <br>
Mitigation: Avoid placing sensitive information in watchlist labels or notes, and clear the local files when the data is no longer needed. <br>
Risk: Cron examples can run recurring checks and alerts. <br>
Mitigation: Add cron jobs only when recurring market checks are intended, and review the scheduled commands before enabling them. <br>
Risk: The paper-trading commands simulate positions and do not execute real trades. <br>
Mitigation: Treat portfolio output as local simulation only; real trading requires separate wallet authentication that this skill does not implement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ShrimpDaddie/polymarket-gonewild) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket documentation](https://docs.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style CLI guidance and plain-text market summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain local watchlist and simulated portfolio JSON files under ~/.polymarket/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
