## Description: <br>
Monitor cryptocurrency and financial markets via exchange APIs (Binance, OKX). Track prices, analyze trends, and generate market reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to answer market-data questions, poll exchange prices, calculate technical indicators, and summarize informational trading signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exchange API credentials may expose account capabilities if broad trading or withdrawal-enabled keys are supplied. <br>
Mitigation: Use a dedicated read-only or market-data-only key, and do not provide trading or withdrawal-enabled credentials. <br>
Risk: Polling and alert workflows can create unnecessary API traffic or hit exchange rate limits if configured too aggressively. <br>
Mitigation: Configure polling intervals and alert conditions explicitly before use. <br>
Risk: Generated trading signals can be mistaken for financial advice. <br>
Mitigation: Treat signals and confidence scores as informational market analysis only. <br>
Risk: OKX secret and passphrase values are sensitive and are not needed for the documented public market-data workflow. <br>
Mitigation: Avoid supplying OKX secret or passphrase values unless a later reviewed workflow clearly requires them. <br>


## Reference(s): <br>
- [Market Monitor on ClawHub](https://clawhub.ai/patches429/market-monitor) <br>
- [Binance](https://www.binance.com) <br>
- [Binance 24h Ticker API](https://api.binance.com/api/v3/ticker/24hr) <br>
- [Binance Klines API](https://api.binance.com/api/v3/klines) <br>
- [OKX Market Ticker API](https://api.okx.com/api/v5/market/ticker) <br>
- [OKX Market Candles API](https://api.okx.com/api/v5/market/candles) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON market report with optional explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pair, exchange, interval, timestamp, price, 24h change, volume, indicators, signal, confidence, and key support and resistance levels.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
