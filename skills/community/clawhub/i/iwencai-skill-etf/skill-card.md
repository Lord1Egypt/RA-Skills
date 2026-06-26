## Description: <br>
同花顺智能选ETF skill。根据行情、跟踪指数基本面、规模、风格类型等条件筛选ETF。返回符合条件的相关ETF数据。当用户询问ETF筛选问题时，必须使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bensema](https://clawhub.ai/user/bensema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to screen ETFs with natural-language conditions such as market data, tracked indexes, fundamentals, fund size, and investment style. Responses should cite 同花顺问财 as the data source and guide users to the official web interface when no data is returned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ETF screening queries are sent to the third-party IWENCAI market-data service using an API token. <br>
Mitigation: Avoid including private portfolio details, account information, or proprietary investment strategy in queries, and keep use scoped to ETF research. <br>
Risk: Returned market data or ETF screening results may be incomplete, unavailable, delayed, or unsuitable as investment advice. <br>
Mitigation: Cite 同花顺问财 as the data source, disclose the final query used after retries, and direct users to the official web interface when no data is returned. <br>


## Reference(s): <br>
- [ETF数据查询接口文档](references/api.md) <br>
- [IWENCAI Query API](https://openapi.iwencai.com/v1/query2data) <br>
- [同花顺问财 Web](https://www.iwencai.com/unifiedwap/chat) <br>
- [ClawHub Skill Page](https://clawhub.ai/bensema/iwencai-skill-etf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text ETF screening answer; CLI output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rewritten query text, ETF result rows, source attribution, retry guidance, and friendly error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
