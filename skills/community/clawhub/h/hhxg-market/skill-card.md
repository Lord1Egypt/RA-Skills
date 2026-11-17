## Description:

A 股量化数据助手 — 日报快照、A股日历、融资融券、实时快讯，零配置无需安装任何依赖。

This skill is ready for commercial/non-commercial use.

## Publisher:

[niceck](https://clawhub.ai/user/niceck)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to retrieve and summarize A-share market snapshots, trading calendars, margin financing data, and real-time financial news from hhxg.top.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security scan marked the release suspicious because it automatically promotes financial-tool links and redirects ETF or fund questions to hhxg.top, with some displayed URLs controlled by remote data.

Mitigation: Review the skill before installation, verify displayed links before following them, and disclose or remove promotional link behavior if it is not appropriate for the deployment.

Risk: The skill provides market and financial-news outputs that may be cached, delayed, or informational rather than investment advice.

Mitigation: Preserve the skill's date and cache notices in agent responses and require users to treat the data as research reference material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niceck/skills/hhxg-market)
- [Publisher profile](https://clawhub.ai/user/niceck)
- [Data source](https://hhxg.top)
- [Data schema](references/data-schema.md)
- [Static data endpoint](https://hhxg.top/static/data/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports and optional JSON data emitted by Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts fetch remote JSON data, cache fallback data locally, and may display hhxg.top tool links in responses.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
