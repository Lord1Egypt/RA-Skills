## Description: <br>
Analyze Polymarket prediction markets for trading edges. Pair Cost arbitrage, whale tracking, sentiment analysis, momentum signals, user profile tracking. No execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukebaze](https://clawhub.ai/user/lukebaze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to analyze Polymarket prediction markets, monitor selected markets for read-only alerts, and inspect wallet positions, trades, and P&L. It supports opportunity identification only and does not execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring market monitors may continue sending alerts after the user no longer needs them. <br>
Mitigation: Enable monitors deliberately, confirm the cron schedule and delivery channel, and remove or disable monitors when monitoring is no longer needed. <br>
Risk: Prediction-market research outputs may be incomplete, stale, or mistaken for execution-ready financial guidance. <br>
Mitigation: Treat outputs as research only, verify market data and resolution rules independently, and rely on the skill's no-execution boundary. <br>
Risk: Monitoring can persist market snapshots in local state files. <br>
Mitigation: Review generated state files and delete them when they are no longer needed for alert comparisons. <br>


## Reference(s): <br>
- [Polymarket Analysis on ClawHub](https://clawhub.ai/lukebaze/polymarket-analysis) <br>
- [Polymarket API Reference](references/polymarket-api.md) <br>
- [Market Monitoring Setup](references/market-monitoring-setup.md) <br>
- [Pair Cost Arbitrage Strategy](references/pair-cost-arbitrage.md) <br>
- [Momentum Analysis Strategy](references/momentum-analysis.md) <br>
- [Whale Tracking Strategy](references/whale-tracking.md) <br>
- [Sentiment Analysis Strategy](references/sentiment-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown analysis, JSON command output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analysis; optional monitors can write local state files and send alerts when explicitly enabled.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
