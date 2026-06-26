## Description: <br>
Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to query Polymarket and Kalshi market data through AIsa, including prices, order books, trades, historical candles, wallet positions, P&L, and cross-platform sports market matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AIsa receives the API key and query history needed to service prediction-market requests. <br>
Mitigation: Install only if the user trusts AIsa with that data, store the API key as a secret, and use a limited or read-only key if AIsa supports it. <br>
Risk: Wallet-address lookups can reveal sensitive financial identifiers and trading history. <br>
Mitigation: Prefer querying only owned or authorized wallets and avoid unnecessary third-party profiling. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chaimengphp/openclaw-aisa-prediction-market) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with bash, curl, Python commands, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; most downstream queries require market identifiers from a prior markets response.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
