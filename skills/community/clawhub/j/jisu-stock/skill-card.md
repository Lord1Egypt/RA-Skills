## Description:

按股票代码查当日行情与详情（分钟级趋势），按分类拉取股票列表，查询交易日历及财务报表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up current stock quotes, stock lists, market trading-calendar status, and financial statement data through JisuAPI-backed commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured Jisu AppKey and requested stock query parameters to JisuAPI.

Mitigation: Install only when that API-key use and data sharing are acceptable; keep JISU_API_KEY scoped and managed as a secret.

Risk: Returned market and financial data is third-party financial information and may be incomplete, delayed, or unsuitable for trading decisions.

Mitigation: Treat results as informational lookup data, verify important outputs against authoritative sources, and do not present responses as trading advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-stock)
- [JisuAPI stock API documentation](https://www.jisuapi.com/api/stock/)
- [JisuAPI website](https://www.jisuapi.com/)
- [Related ClawHub stock history skill](https://clawhub.ai/jisuapi/stockhistory)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [JSON responses with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends stock codes, dates, and financial-query parameters to JisuAPI.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
