## Description:

按日期查询上海黄金交易所历史行情，返回品种、开盘价、最高价、最低价、收盘价、涨跌幅和成交量等信息，数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Shanghai Gold Exchange historical quote data for a specified YYYY-MM-DD date and return a readable table or raw JSON. Results are informational only and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable API base URL can redirect requests and expose the API key to an unintended server.

Mitigation: Run the skill only where JIKE_API_BASE_URL cannot be set by untrusted parties and use a dedicated low-privilege Jike API key.

Risk: Supplying the API key on the command line can expose it through shell history or process listings.

Mitigation: Prefer JIKE_GOLD_SHGOLD_QUERY_KEY or JIKE_APPKEY environment variables instead of the --key argument.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-gold-shgold-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Shanghai Gold Exchange history API endpoint](https://api.jikeapi.cn/v1/gold/shgold/history)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text table or JSON, typically summarized in Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a query date and a Jike API key; the skill reminds users that market data is not investment advice.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
