## Description:

通过 AIsa API 查询 Polymarket 和 Kalshi 的预测市场行情、价格、订单簿、K线、持仓、交易记录及跨平台体育市场数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external analysts use this skill to query read-only prediction market data, compare Polymarket and Kalshi markets, and inspect prices, order books, wallet activity, positions, P&L, and sports market matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a paid AIsa API key and any wallet addresses or market query parameters used in commands to api.aisa.one.

Mitigation: Use a limited or revocable API key, monitor usage costs, and avoid sending wallet identifiers or queries that are not needed for the task.

Risk: Server security evidence flags disclosure and credential-safety gaps for users to review before installation.

Mitigation: Review the skill before deployment and ask the publisher for clearer privacy and permission metadata and same-origin redirect protection.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/prediction-market-data-zh)
- [AIsa](https://aisa.one)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [Polymarket](https://polymarket.com)
- [Kalshi](https://kalshi.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; responses may include usage cost and credits remaining.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
