## Description: <br>
Uses AIsa API market data to identify cross-platform arbitrage opportunities between Polymarket and Kalshi, compare prices, and check order book depth before action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, traders, and developers use this skill to scan sports prediction markets, compare Polymarket and Kalshi prices, and validate liquidity before considering an arbitrage trade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet and P&L lookup commands can send supplied Polymarket wallet addresses or other financial identifiers to AIsa. <br>
Mitigation: Do not provide wallet addresses or identifiers unless the user explicitly accepts sending them to the third-party API. <br>
Risk: AISA_API_KEY usage may incur per-query costs. <br>
Mitigation: Monitor API usage and credits before running broad scans or repeated market queries. <br>
Risk: Detected price spreads may not be executable if order book depth is insufficient. <br>
Mitigation: Use the provided order book commands to verify liquidity before acting on any arbitrage result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/prediction-market-arbitrage-zh) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [Polymarket](https://polymarket.com) <br>
- [Kalshi](https://kalshi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an AISA_API_KEY environment variable; API calls are made over HTTPS to AIsa.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
