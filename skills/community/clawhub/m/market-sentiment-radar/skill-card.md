## Description:

A股市场环境与情绪研究。用于盘前简报、大盘体检、板块轮动和跨市场信息整理。先核验数据来源与日期；证据不足时不判定周期、不评分。不用于自动荐股或下单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgetao730](https://clawhub.ai/user/georgetao730)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market researchers use this skill to generate Chinese-language China A-share market environment notes from dated public index data. It supports pre-market or post-close review, source/date checking, and explicit handling of missing evidence rather than automated trading decisions.

### Deployment Geography for Use:

Global, with market coverage focused on China A-share public market data.

## Known Risks and Mitigations:

Risk: Public market-data requests through AKShare may be unavailable, delayed, or incomplete.

Mitigation: Review reported source dates, missing fields, and errors before using the report, and stop market conclusions when data is unavailable.

Risk: Market research output may be mistaken for trading advice or authorization for account actions.

Mitigation: Use the output for information only, avoid automatic trading or portfolio changes, and require separate explicit authorization for any account action.

## Reference(s):

- [Data and Analysis Method](references/research-method.md)
- [Risk Boundaries](references/position-mapping.md)
- [AKShare index data documentation](https://akshare.akfamily.xyz/data/index/index.html)
- [Eastmoney market data source](https://quote.eastmoney.com/)
- [Sina Finance market data source](https://finance.sina.com.cn/)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Chinese plain-text market research report, with optional JSON output when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output; reports source dates, missing data, and errors, and states that the result is not investment advice.]

## Skill Version(s):

1.3.2 (source: server release evidence and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
