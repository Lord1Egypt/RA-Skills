## Description:

使用自然语言查询金融数据，支持A股股票、基金、期货等上市品种，覆盖基本资料、财务数据、日频行情信息、持仓信息及各类分析指标等数据。也支持宏观经济数据，包括世界经济数据、全球经济数据、中国经济数据、区域经济数据、行业经济数据、利率走势数据、商品数据和特色数据等。当需要查询上述金融相关数据查询时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenzisay](https://clawhub.ai/user/wenzisay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer finance-data questions through natural-language queries for equities, funds, futures, market data, financial statements, analysis indicators, holdings, and macroeconomic data. The skill returns concise conclusions and preserves tables when tabular data is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an API token in local configuration and can be configured to send that token to a custom URL.

Mitigation: Install only if the publisher and iFind Repilot endpoint are trusted; avoid custom URLs unless controlled and trusted, rotate any token used with an untrusted URL, and treat the config file and shell history as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenzisay/skills/ifind-repilot-finance-data-search)
- [iFind Repilot platform](https://repilot.51ifind.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown tables, with shell commands for setup and execution guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a configured iFind Repilot auth token; results depend on endpoint availability, token validity, usage limits, and data permissions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
