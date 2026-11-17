## Description:

Use this skill to call the Kronos Crypto Data API, a pay-per-call real-time crypto market data API that uses x402 USDC micropayments on Base mainnet for prices, derivatives signals, forecasts, alerts, market snapshots, OHLC data, volatility, and funding screens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vizionik25](https://clawhub.ai/user/vizionik25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to query Kronos Crypto Data API endpoints for crypto market data, derivatives intelligence, forecasts, alerts, and related market context. The skill is intended for informational market analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may make wallet-signed paid USDC API calls.

Mitigation: Use a dedicated low-balance wallet, enforce spend caps outside the skill, and require explicit confirmation before recurring or automated paid calls.

Risk: Market signals and forecasts may be incorrect, stale, or misused as financial advice.

Mitigation: Treat outputs as informational analysis only, verify important decisions against independent sources, and preserve the skill's financial-advice disclaimer in agent responses.

Risk: Payment helpers require signing access for x402 EIP-3009 transfers.

Mitigation: Verify any payment helper before granting wallet access and avoid caching or reusing payment tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vizionik25/skills/kronos-signals-api)
- [Kronos Crypto Data API](https://kronossignals.com)
- [OpenAPI specification](https://kronossignals.com/api/openapi.json)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with endpoint URLs, HTTP request examples, payment flow instructions, and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes paid endpoint costs, supported crypto assets, error handling guidance, and informational-use disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill overview)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
