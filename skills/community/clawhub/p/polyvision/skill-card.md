## Description:

PolyVision helps agents analyze Polymarket wallets, compare trader performance, inspect risk metrics and recent trades, discover top traders and hot bets, and retrieve guidance through MCP or REST.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mysticriverx](https://clawhub.ai/user/mysticriverx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use PolyVision to evaluate Polymarket traders, compare wallets, inspect risk and performance signals, discover high-performing traders, and review recent market activity before copy-trading decisions. The skill is advisory for market analysis; saved-portfolio and API-key operations change PolyVision account state, not blockchain assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PolyVision receives an API key, wallet queries, and account metadata.

Mitigation: Install only when the publisher is trusted, keep POLYVISION_API_KEY secret, and avoid sending unnecessary wallet or account context.

Risk: Portfolio add/remove tools and API-key regenerate/deactivate tools change PolyVision account state.

Mitigation: Require clear user confirmation before adding or removing tracked wallets, regenerating an API key, or deactivating an API key.

Risk: Wallet analytics and copy-trading guidance may influence financial decisions.

Mitigation: Treat outputs as decision support, verify important findings independently, and do not present the skill as placing trades or moving funds.

## Reference(s):

- [PolyVision Skill Page](https://clawhub.ai/mysticriverx/skills/polyvision)
- [PolyVision Homepage](https://polyvisionx.com)
- [PolyVision Docs](https://polyvisionx.com/docs)
- [PolyVision API Docs](https://api.polyvisionx.com/docs)
- [PolyVision OpenAPI JSON](https://api.polyvisionx.com/openapi.json)
- [Response Schemas](references/response-schemas.md)
- [PolyVision Bot](https://t.me/PolyVisionBot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP or REST response summaries for wallet analytics, risk metrics, leaderboard entries, portfolio state, API-key status, and account-action confirmations.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
