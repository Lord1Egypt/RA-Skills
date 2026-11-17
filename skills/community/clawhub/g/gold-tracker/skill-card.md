## Description:

A zero-dependency gold price tracking skill for AI agents that fetches live gold prices and USD/CNY rates, validates sourced market analysis, detects dynamic price breakouts, archives logs, and generates briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeromeex](https://clawhub.ai/user/jeromeex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run recurring gold market monitoring, collect public market data and news, enforce source-backed analysis, and send local or configured notifications when price movement crosses configured thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured notification commands can run with the process environment and may send content externally.

Mitigation: Review config.yaml before installation, keep the default file notifier unless the destination and command are trusted, and avoid running with sensitive environment variables.

Risk: Cron or systemd scheduling can create recurring network fetches and automatic notifications.

Mitigation: Enable scheduled execution only when recurring fetches and notifications are intended, and keep notifier retry, timeout, and rate-limit settings aligned with operational needs.

Risk: Fetch logs alone do not prove that a cited source was truly fetched or still supports the analysis.

Mitigation: Review generated market analyses and verify important source URLs before relying on conclusions.

## Reference(s):

- [ClawHub Gold Tracker release](https://clawhub.ai/jeromeex/skills/gold-tracker)
- [GoldPriceZ default gold price source](https://goldpricez.com)
- [ExchangeRate-API open USD rates endpoint](https://open.er-api.com/v6/latest/USD)
- [MINING.COM RSS feed](https://www.mining.com/feed/)
- [Oilprice RSS feed](https://oilprice.com/rss/main)
- [FXStreet news RSS feed](https://www.fxstreet.com/rss/news)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML/JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces source-backed YAML analysis logs, alert records, summaries, archives, and notification messages; analysis checks reject unsupported claims.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
