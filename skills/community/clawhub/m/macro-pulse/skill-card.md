## Description:

每日宏观数据监控与推送机器人，巡检公开宏观数据、政策和财经资讯源，整合过去 24 小时信息并生成带科普解读的推送报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation operators use this skill to run daily macroeconomic monitoring, summarize notable data and policy changes, explain indicators in plain language, and send the resulting report through an agent-supported messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs and outbound report delivery can send macro reports to the wrong channel or recipient if messaging targets are not reviewed.

Mitigation: Confirm IM, email, or webhook destinations before enabling cron delivery, and test with a limited recipient first.

Risk: The skill may update local support files such as source health, indicator, watchlist, or report files during normal operation.

Mitigation: Limit writable paths to the intended skill reference and report locations, and review changes after initial runs.

Risk: Broad delete, reset, import, or modification wording is not tightly scoped in the artifact.

Mitigation: Constrain or ignore those generic operations unless the publisher documents exact safe commands and expected affected files.

Risk: Macro data and policy summaries may be incomplete or misleading when public sources fail, change structure, or return delayed data.

Mitigation: Keep source health warnings in the report, cross-check material indicators against authoritative sources, and review high-impact alerts before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/macro-pulse)
- [Trading Economics economic calendar](https://tradingeconomics.com/calendar)
- [FRED releases](https://fred.stlouisfed.org/releases)
- [National Bureau of Statistics of China](http://www.stats.gov.cn/)
- [People's Bank of China](http://www.pbc.gov.cn/)
- [China Securities Regulatory Commission](http://www.csrc.gov.cn/)
- [Cailian Press](https://www.cls.cn/)
- [Wallstreetcn](https://wallstreetcn.com/)
- [FRED API key documentation](https://fred.stlouisfed.org/docs/api/api_key.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report text with optional scheduling and messaging configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include source health status, GMT+8 time-window handling, highlighted macro events, indicator explanations, policy notes, news summaries, and delivery status when available.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
