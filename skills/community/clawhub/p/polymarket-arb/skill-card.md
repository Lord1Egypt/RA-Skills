## Description: <br>
Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to find matching Polymarket and Kalshi markets, compare prices, and check liquidity before evaluating prediction-market spread opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AIsa API keys may incur query costs or expose access if reused broadly. <br>
Mitigation: Use a scoped or throwaway AIsa API key where possible, monitor usage costs and remaining credits, and rotate the key if it is exposed. <br>
Risk: Wallet lookup features can involve sensitive user context if private credentials are supplied. <br>
Mitigation: Provide only public wallet addresses for wallet lookups and never provide private keys, seed phrases, or exchange credentials. <br>
Risk: Example cURL commands contain placeholders that can fail or execute unintended requests if left unresolved. <br>
Mitigation: Before executing cURL commands, replace every placeholder such as token_id, market_ticker, sport, and date with a concrete value. <br>
Risk: Reported spreads may be misleading if liquidity, fees, or slippage are not reviewed. <br>
Mitigation: Use the orderbook endpoints and review market depth before treating a spread as actionable. <br>


## Reference(s): <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [AIsa](https://aisa.one) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/aisadocs/polymarket-arb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with cURL examples and Python CLI/API code; scripts can return JSON responses from the AIsa API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and uses read-only prediction-market API calls; artifact metadata lists curl and python3 as runtime dependencies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
