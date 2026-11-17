## Description:

Meteora liquidity analyst for OpenClaw that queries Meteora public APIs for DLMM, DAMM v1, and DAMM v2 pool, liquidity, APR, TVL, volume, fee, and protocol metrics on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelespinoza](https://clawhub.ai/user/angelespinoza)

### License/Terms of Use:

MIT-0

## Use Case:

External users, DeFi researchers, Solana traders, and developers use this skill to query Meteora public REST APIs and compare pools, token liquidity, rankings, protocol metrics, and LP trade-offs. The skill is informational only and does not access wallets or execute transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide DeFi liquidity analysis that may be mistaken for financial advice.

Mitigation: Present outputs as informational analysis, include pool and market risks, and encourage users to verify data before making liquidity decisions.

Risk: Live public API data may change, be rate limited, or be temporarily unavailable.

Mitigation: Query the APIs at response time, report data freshness or request failures clearly, and avoid inventing missing metrics.

Risk: Activation wording may lead the agent to answer broader non-Meteora Solana liquidity questions.

Mitigation: Keep use focused on Meteora DLMM, DAMM v1, DAMM v2, pool metrics, and protocol-level Meteora analysis.

## Reference(s):

- [Meteora API Endpoints](references/api-endpoints.md)
- [Meteora Liquidity Analyst on ClawHub](https://clawhub.ai/angelespinoza/skills/meteora-analyst)
- [DLMM API](https://dlmm.datapi.meteora.ag)
- [DAMM v1 API](https://amm-v2.meteora.ag)
- [DAMM v2 API](https://damm-v2.datapi.meteora.ag)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with tables and inline JavaScript or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live public Meteora API responses; no wallet, API key, or configuration is required.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact metadata states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
