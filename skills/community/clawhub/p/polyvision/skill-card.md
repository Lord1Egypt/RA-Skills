## Description: <br>
PolyVision helps agents analyze Polymarket wallets, compare trader performance, inspect risk metrics and red flags, find leaderboard traders and hot bets, and manage a saved tracked-wallet portfolio through MCP or REST APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mysticriverx](https://clawhub.ai/user/mysticriverx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to research Polymarket wallets, evaluate copy-trading candidates, compare risk and performance, inspect recent trades and open positions, and configure PolyVision MCP or REST access. It is for analytics and account-scoped watch-list management, not on-chain trading or fund movement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends wallet-analysis requests to PolyVision's hosted service using a PolyVision API key. <br>
Mitigation: Install only when comfortable sharing those requests with PolyVision, store POLYVISION_API_KEY securely, and rotate or deactivate the key if access should change. <br>
Risk: Portfolio add and remove operations change the user's PolyVision tracked-wallet watch list. <br>
Mitigation: Call add_to_portfolio or remove_from_portfolio only after the user explicitly asks to save, track, untrack, remove, or delete a wallet. <br>
Risk: API-key regeneration invalidates the old key, and deactivation rejects future requests with the current key. <br>
Mitigation: Require explicit confirmation before regenerate_key or deactivate_key and remind the user to update MCP or REST configuration after regeneration. <br>
Risk: Trading scores, strategy profiles, leaderboards, and hot bets can be mistaken for investment advice. <br>
Mitigation: Present PolyVision output as financial research only and avoid representing analytics as instructions to trade or guarantees of future performance. <br>


## Reference(s): <br>
- [PolyVision ClawHub listing](https://clawhub.ai/mysticriverx/polyvision) <br>
- [PolyVision publisher profile](https://clawhub.ai/user/mysticriverx) <br>
- [PolyVision homepage](https://polyvisionx.com) <br>
- [PolyVision API documentation](https://polyvisionx.com/docs) <br>
- [PolyVision OpenAPI specification](https://api.polyvisionx.com/openapi.json) <br>
- [Response schemas](references/response-schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration, shell command examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POLYVISION_API_KEY for authenticated MCP or REST calls; some data tools require Premium or an active trial.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
