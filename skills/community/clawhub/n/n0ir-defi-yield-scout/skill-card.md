## Description:

Scan and compare USDC yield farming options on Base and Arbitrum with APY rankings, breakeven analysis, historical trends, and protocol risk summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joaoolucas](https://clawhub.ai/user/joaoolucas)

### License/Terms of Use:


## Use Case:

External users and DeFi analysts use this skill to compare USDC yield opportunities across Base and Arbitrum, inspect protocol risk notes, evaluate APY history, and estimate whether a vault move may be worthwhile. Outputs are informational and should be verified before moving funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yield results are advisory and can differ from current on-chain conditions.

Mitigation: Verify pools, APYs, TVL, and protocol status on-chain or with the source protocol before moving funds.

Risk: The local pool cache is a low-level integrity risk and may be stale or modified on shared systems.

Mitigation: Treat cached results as temporary, refresh data before acting, and prefer a future version that stores cache files in a private per-user cache directory.

Risk: Gas, bridge, and breakeven estimates are approximate.

Mitigation: Check live gas, bridge fees, slippage, and withdrawal timing before migrating between vaults or chains.

## Reference(s):

- [Protocol Reference](references/protocols.md)
- [DeFiLlama Yield Pools API](https://yields.llama.fi/pools)
- [DeFiLlama Yield Chart API](https://yields.llama.fi/chart/{pool_id})
- [n0ir](https://n0ir.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json, guidance]

**Output Format:** [Markdown summaries with tables and optional JSON output from CLI subcommands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public DeFiLlama yield data; pool data may be cached locally for 15 minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
