## Description: <br>
Meteora liquidity analyst for OpenClaw that queries public Meteora APIs for DLMM, DAMM v1, and DAMM v2 data to answer questions about Solana pools, liquidity, APR, TVL, volume, and fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angelespinoza](https://clawhub.ai/user/angelespinoza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, DeFi researchers, Solana traders, and developers use this skill to inspect Meteora liquidity pools, compare DLMM and DAMM markets, rank pools by APR, TVL, volume, or fees, and review protocol metrics before making independent decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APR, liquidity, volume, and pool recommendations are informational and can become stale or misleading as market conditions change. <br>
Mitigation: Query live Meteora public APIs at response time, include context such as TVL, volume, fees, and token verification, and avoid presenting results as financial advice. <br>
Risk: Broad Solana liquidity requests may be routed to the wrong data source or interpreted outside the skill's Meteora scope. <br>
Mitigation: Specify Meteora, DLMM, DAMM v1, or DAMM v2 when asking liquidity questions and disclose when an answer is limited to Meteora public API data. <br>
Risk: DAMM v1 coverage is narrower because the documented API requires a pool address and does not support unfiltered listings. <br>
Mitigation: Ask for or provide a DAMM v1 pool address for DAMM v1 details, and use DLMM or DAMM v2 endpoints for broader pool discovery and rankings. <br>


## Reference(s): <br>
- [Meteora API Endpoints](references/api-endpoints.md) <br>
- [ClawHub release page](https://clawhub.ai/angelespinoza/meteora-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with tables, inline code examples, and optional JSON-derived metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live public Meteora REST API data; no wallet, API key, credentials, or transaction authority are requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
