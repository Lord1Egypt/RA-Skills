## Description:

Global Intel Summary helps an agent generate structured Chinese-language global market, political, geopolitical, and AI news intelligence reports with source attribution and freshness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmsx000-cloud](https://clawhub.ai/user/gmsx000-cloud)

### License/Terms of Use:

MIT

## Use Case:

External users and analysts can use this skill to ask an agent for current Chinese-language summaries of markets, public news, geopolitical events, AI developments, and near-term risk signals. The skill is intended for structured reporting and triage, with important financial or geopolitical claims verified independently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live public web, RSS, and market-data lookups can return stale, incomplete, or conflicting information.

Mitigation: Require timestamps and source labels in the report, and independently verify important financial or geopolitical claims with authoritative sources.

Risk: The package gives broad reporting instructions, while the included helper script covers only a narrow subset of market data.

Mitigation: Treat unsupported sections as agent-generated summaries that require source review, not as guaranteed outputs from the helper script.

Risk: Financial and geopolitical summaries may be misused as decision-ready advice.

Mitigation: Use the report for triage and situational awareness, and require human review before acting on market, policy, or security-sensitive claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmsx000-cloud/skills/global-intel-summary)
- [BBC World RSS](https://feeds.bbci.co.uk/news/world/rss.xml)
- [Yahoo Finance RSS](https://finance.yahoo.com/news/rssindex)
- [Federal Reserve press feed](https://www.federalreserve.gov/feeds/press_all.xml)
- [CSIS analysis feed](https://www.csis.org/analysis/feed)
- [CISA alerts feed](https://www.cisa.gov/uscert/ncas/alerts.xml)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true)
- [Yahoo Finance Nasdaq chart API](https://query1.finance.yahoo.com/v8/finance/chart/^IXIC)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report in zh-CN, with source labels and timestamps for data points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include alert labels, region tags, narrative tracking, and risk notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; skill frontmatter and changelog describe content version 3.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
