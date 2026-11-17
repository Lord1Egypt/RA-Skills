## Description:

Full-stack Orca Whirlpool agent - read-only pool analytics (discovery, ranking, 6-month stability, range sizing, Monte Carlo projection, retrospective yield, rebalance planning, exit planning) plus on-chain liquidity management (open, increase, decrease, collect fees, close, swap). Wallet only required for intentional writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaizen-orca](https://clawhub.ai/user/kaizen-orca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Orca Whirlpool pools on Solana, compare liquidity opportunities, size LP ranges, estimate historical yield, plan rebalances or exits, and generate scripts for intentional liquidity or swap operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated write scripts can submit wallet-signed financial transactions.

Mitigation: Use a small dedicated wallet, keep KEYPAIR_PATH unset for analytics, review generated scripts, and add an explicit confirmation check at the transaction-send boundary before execution.

Risk: Pool analytics and yield estimates can be misleading if treated as recommendations or predictions.

Mitigation: Present retrospective yield, volatility, range containment, slippage, token addresses, and caveats together, and avoid treating APR or Monte Carlo output as expected return.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaizen-orca/skills/orca-lp-analytics)
- [Orca REST API](https://api.orca.so/v2/solana)
- [Orca Beachhouse analytics API](https://stats-api.mainnet.orca.so)
- [Orca Snorkel quote API](https://pools-api.mainnet.orca.so)
- [Solana RPC](https://api.mainnet-beta.solana.com)
- [Scan pools example](examples/scan-pools.md)
- [LP range analysis example](examples/lp-range-analysis.md)
- [Open position example](examples/open-position.md)
- [Manage position example](examples/manage-position.md)
- [Swap example](examples/swap.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analytics do not require a wallet; intentional write operations require KEYPAIR_PATH and should be reviewed before execution.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact metadata reports 4.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
