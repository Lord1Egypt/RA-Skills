## Description:

同花顺智能选ETF skill。根据行情、跟踪指数基本面、规模、风格类型等条件筛选ETF。返回符合条件的相关ETF数据。当用户询问ETF筛选问题时，必须使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bensema](https://clawhub.ai/user/bensema)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn natural-language ETF screening requests into iWenCai ETF queries and summarize matching ETF data. It is suited for ETF screening by market metrics, tracked index, fundamentals, fund scale, style, and combined conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an iWenCai API key.

Mitigation: Use IWENCAI_API_KEY from the environment and avoid passing API keys on the command line.

Risk: ETF queries are sent to an external iWenCai API.

Mitigation: Avoid sending sensitive investment strategies or confidential financial information in queries.

Risk: The skill may invoke other financial or search tools when data is incomplete.

Mitigation: Constrain available tools in the runtime when external calls must be limited.

Risk: Security evidence marks the release as suspicious pending review.

Mitigation: Review the skill before installing and scan it before deployment.

## Reference(s):

- [ETF API reference](references/api.md)
- [iWenCai query API](https://openapi.iwencai.com/v1/query2data)
- [iWenCai web query](https://www.iwencai.com/unifiedwap/chat)
- [ClawHub skill release](https://clawhub.ai/bensema/skills/iwencai-skill-etf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown or JSON with ETF query results and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IWENCAI_API_KEY for API access; responses should identify iWenCai as the data source.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
