## Description: <br>
Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and autonomous agents use this skill to match prediction-market events across Polymarket and Kalshi, compare prices, calculate arbitrage spreads, and inspect orderbook liquidity before acting on an opportunity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled client includes wallet portfolio, activity, orders, and P&L lookups that send supplied Polymarket wallet identifiers to AIsa. <br>
Mitigation: Use wallet commands only for addresses the user is comfortable sharing with AIsa, and keep arbitrage-only workflows focused on market, price, matching, and orderbook endpoints. <br>
Risk: AIsa API requests may consume paid credits and expose query details to the API provider. <br>
Mitigation: Set AISA_API_KEY only in trusted environments, review commands before execution, and monitor usage.cost and credits_remaining in responses. <br>
Risk: The cURL examples use placeholder values that can fail or be misinterpreted if executed literally. <br>
Mitigation: Replace every placeholder such as {token_id}, {market_ticker}, {sport}, and {date} with concrete values before running curl, and fail fast if placeholders remain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaimengphp/openclaw-aisa-prediction-market-arbitrage) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with cURL and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; market identifiers should be looked up before downstream price or orderbook calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
