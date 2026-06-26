## Description: <br>
Cross-platform prediction market data via AIsa API. Query Polymarket and Kalshi markets, prices, orderbooks, candlesticks, positions, and trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to search prediction markets, retrieve prices and orderbook data, review wallet-visible market activity, and compare Polymarket and Kalshi sports markets through read-only API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AIsa API key and uses it for outbound API requests. <br>
Mitigation: Use a scoped API key where available, store it only in the AISA_API_KEY environment variable, and rotate it if it may have been exposed. <br>
Risk: AIsa queries may incur usage charges. <br>
Mitigation: Run narrow searches first, set conservative limits, and review returned usage cost and remaining credits. <br>
Risk: Wallet commands can query public wallet activity, positions, and PnL. <br>
Mitigation: Only provide wallet addresses when public wallet lookup is intended and avoid treating returned market data as private account verification. <br>
Risk: Prediction market prices can be stale, illiquid, or misleading if interpreted as certainty. <br>
Mitigation: Check market status, timestamp, volume, and liquidity before relying on odds for analysis or decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/prediction-market-data) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [AIsa](https://aisa.one) <br>
- [Polymarket](https://polymarket.com) <br>
- [Kalshi](https://kalshi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only HTTPS GET requests require AISA_API_KEY and may include public wallet addresses when wallet activity, positions, or PnL are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
