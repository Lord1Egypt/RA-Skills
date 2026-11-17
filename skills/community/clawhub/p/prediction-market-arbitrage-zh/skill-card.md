## Description:

通过 AIsa API 发现 Polymarket 和 Kalshi 预测市场的套利机会，扫描体育市场跨平台价差、比较实时赔率并验证订单簿流动性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to scan prediction-market data for cross-platform price differences between Polymarket and Kalshi. It supports market search, odds comparison, arbitrage analysis, and orderbook liquidity checks before any separate trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated AIsa requests may be paid and consume credits.

Mitigation: Set AISA_API_KEY only in environments approved for paid AIsa use and monitor usage cost and remaining credits in responses.

Risk: Wallet analytics commands can send wallet addresses and financial-profile queries to AIsa.

Mitigation: Avoid wallet activity, wallet, positions, orders --user, and P&L commands unless the user intentionally authorizes those wallet identifiers to be queried.

Risk: The scanner classified the release as suspicious because wallet-query capability is broader than the SKILL.md disclosure.

Mitigation: Review the scanner summary before deployment and restrict use to read-only market, price, matching, and orderbook queries when wallet analytics are out of scope.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/prediction-market-arbitrage-zh)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa](https://aisa.one)
- [Polymarket](https://polymarket.com)
- [Kalshi](https://kalshi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; AIsa requests are authenticated and may be paid.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
