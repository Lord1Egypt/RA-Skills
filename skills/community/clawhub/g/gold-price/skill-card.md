## Description:

查询当前黄金大盘价格。用于回答关于黄金价格、金价走势、贵金属行情的问题。包括国内金价（银行金条、回收价、首饰品牌价）和国际金价。不需要 API key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojuhao1020-debug](https://clawhub.ai/user/xiaojuhao1020-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current gold and precious-metal price data, especially domestic bank gold bars, jewelry brand prices, and recycle prices. It is for price lookup and summary, not historical market analysis or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Price data may be delayed, unavailable, or different from official transaction quotes.

Mitigation: Present prices as reference-only and advise users to verify with official banks, jewelry brands, exchanges, or other authoritative channels before any transaction or investment decision.

Risk: The skill depends on an external public API for current prices.

Mitigation: Disclose the external API dependency, avoid sending sensitive user data, and handle failed, stale, or malformed API responses before presenting results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaojuhao1020-debug/skills/gold-price)
- [Gold Price API Endpoint](https://v2.xxapi.cn/api/goldprice)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with curl commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; jq is used in optional parsing examples; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
