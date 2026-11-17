## Description:

Macro News Signal is an intelligent market analysis skill that transforms real-time global news and key macro indicators into actionable investment insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhelincheng](https://clawhub.ai/user/zhelincheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to gather global financial news and macro indicators, analyze sentiment and event impact, and produce structured market signal reports for investment decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound requests to third-party finance and news sites may expose request metadata or retrieve untrusted content.

Mitigation: Use the skill only where this network access is acceptable, and prefer vetted sources documented in artifact/references/news_apis.md.

Risk: The Yahoo Finance formatter fetches a caller-provided URL, which can be risky if the URL is user-supplied or untrusted.

Mitigation: Pass only vetted Yahoo Finance API URLs and enforce a strict host allowlist in the execution environment.

Risk: Buy, hold, and sell signals may be mistaken for personalized financial advice.

Mitigation: Treat generated signals as informational market analysis and review them with appropriate financial judgment before acting.

## Reference(s):

- [Macro News Signal on ClawHub](https://clawhub.ai/zhelincheng/skills/macro-news-signal)
- [News API Reference](artifact/references/news_apis.md)
- [Output Format Reference](artifact/references/output_format.md)
- [Folo Feed Reference](https://app.folo.is/share/feeds/70844804758158336)
- [RSSHub Public Instances](https://docs.rsshub.app/zh/guide/instances)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown reports with tables, linked news items, signal ratings, and optional JSON-formatted market data from the Yahoo Finance formatter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational, time-sensitive market analyses that may depend on external RSS, news, market-data, and finance API sources.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
