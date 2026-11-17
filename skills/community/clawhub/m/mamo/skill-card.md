## Description:

Interact with Mamo DeFi yield strategies on Base (Moonwell). Deposit/withdraw USDC, cbBTC, MAMO, or ETH into automated yield strategies. Check APY rates and account status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anajuliabit](https://clawhub.ai/user/anajuliabit)

### License/Terms of Use:


## Use Case:

External DeFi users and developers use this skill to create, inspect, deposit into, and withdraw from Mamo yield strategies on Base, and to check APY and portfolio status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can move real Base mainnet funds through wallet signing, token approvals, deposits, and withdrawals.

Mitigation: Use a dedicated low-balance hot wallet, review each transaction before signing, and run dry-run checks before executing asset-moving commands.

Risk: Changed local strategy-address configuration could route approvals or deposits to an unsafe contract.

Mitigation: Protect and review the local strategy configuration, treat local entries as hints, and verify registry membership, ownership, and trusted provenance on-chain before asset-moving operations.

Risk: Private wallet keys are required for signing and can expose funds if stored in shared or committed files.

Mitigation: Keep MAMO_WALLET_KEY out of committed files and shared workspaces, and rotate the wallet if the key may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anajuliabit/skills/mamo)
- [Mamo](https://mamo.xyz)
- [Moonwell](https://moonwell.fi)
- [Mamo Contract Addresses and ABIs](references/contracts.md)
- [Mamo API Reference](references/mamo-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may initiate wallet signing, token approvals, deposits, withdrawals, and Base mainnet reads when executed by the user.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
