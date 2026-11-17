## Description:

使用 data.diemeng.chat 提供的接口查询股票日线、分钟线、财务指标等数据，支持 A 股等市场。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1018466411](https://clawhub.ai/user/1018466411)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query A-share market data from data.diemeng.chat, including daily bars, intraday bars, financial factors, valuation data, trading calendars, snapshots, bonds, ETFs, and indexes. It is useful for market-data retrieval and analysis workflows where the user supplies an authorized STOCK_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a STOCK_API_KEY and market-data queries to data.diemeng.chat.

Mitigation: Use the skill only when you trust that service, provide the key through environment or platform secret configuration, and avoid hardcoding it in files.

Risk: Market-data requests may reveal the securities, date ranges, and analysis interests being queried.

Mitigation: Limit outbound traffic to the documented API domain where possible and avoid querying sensitive portfolios unless the data-sharing risk is acceptable.

Risk: Large intraday, tick, or multi-asset queries can create excessive API usage or trigger rate limits.

Mitigation: Use scoped date ranges, pagination, caching, and request throttling; prompt the user to narrow broad requests before calling high-volume endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1018466411/skills/openclaw-stock-data-skill)
- [data.diemeng.chat API Service](https://data.diemeng.chat/)
- [OpenClaw Skills Config](https://docs.openclaw.ai/tools/skills-config)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, Python code examples, shell commands, and tabular or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STOCK_API_KEY and outbound HTTPS access to data.diemeng.chat.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact/skill.json, artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
