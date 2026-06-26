## Description: <br>
Autonomous Polymarket weather-market trading flow for AION Market agents that can derive credentials, select active weather markets, submit default market orders, and verify results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssj124](https://clawhub.ai/user/ssj124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a one-shot AION Market and Polymarket weather-market trade after providing an AION API key and wallet private key. The flow covers balance, gas, allowance, market selection, order submission, and result verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to handle a raw wallet private key and AION API key. <br>
Mitigation: Use a fresh, minimally funded wallet, keep secrets out of logs, and rotate or revoke credentials after use. <br>
Risk: The skill can approve token allowances and place real Polymarket trades without transaction-level confirmation. <br>
Mitigation: Require manual confirmation for each allowance and trade, verify spender and allowance amount, set small limits, and revoke allowances after trading. <br>
Risk: Weather-market selection or trade verification can be incomplete or wrong. <br>
Mitigation: Review the selected market snapshot, order size, price cap, balance, gas, and Polymarket verification result before relying on the outcome. <br>


## Reference(s): <br>
- [AION Market](https://aionmarket.com) <br>
- [AION Market Documentation](https://docs.aionmarket.com) <br>
- [Polymarket Gamma Weather Markets API](https://gamma-api.polymarket.com/events/pagination?tag_slug=weather&active=true&closed=false&archived=false&order=volume24hr&ascending=false&limit=20&offset=0) <br>
- [Polymarket CLOB Endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with Python code snippets and API payload details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIONMARKET_API_KEY and WALLET_PRIVATE_KEY; default order mode is a 2 USDC market buy unless the user overrides it.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata, skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
