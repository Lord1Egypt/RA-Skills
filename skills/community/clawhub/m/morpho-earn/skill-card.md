## Description:

Earn yield on USDC by supplying to the Moonwell Flagship USDC vault on Morpho (Base). Use when depositing USDC, withdrawing from the vault, checking position/APY, or setting up wallet credentials for DeFi yield.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyoungblood](https://clawhub.ai/user/lyoungblood)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to configure a Base wallet, monitor USDC vault positions, deposit or withdraw USDC, claim rewards, and optionally compound rewards back into the Moonwell Flagship USDC vault on Morpho.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create recurring real-money wallet transactions through deposit, withdrawal, reward claim, swap, and compound operations.

Mitigation: Install only with a dedicated low-balance hot wallet and review the configured wallet address before every write operation.

Risk: Auto-compound or HEARTBEAT.md automation may execute repeated transactions before explicit caps and confirmation prompts are in place.

Mitigation: Keep auto-compound disabled until transaction caps, confirmation prompts, and clear approval boundaries are configured.

Risk: Reward compounding depends on assembled Odos swap transactions and external quote data.

Mitigation: Review swap previews, use strict slippage and amount limits, and avoid broad allowances.

Risk: Wallet secrets are loaded locally from a file, environment variable, or 1Password item.

Mitigation: Use encrypted storage or 1Password where possible, restrict file permissions, and never use a primary wallet private key.

Risk: Dependency or API changes may affect on-chain transaction behavior.

Mitigation: Prefer pinned dependencies, review dependency updates, and run status or simulation checks before sending transactions.

## Reference(s):

- [Wallet Setup](references/setup.md)
- [Moonwell Docs](https://docs.moonwell.fi/moonwell/moonwell-overview/vaults)
- [Morpho](https://morpho.org)
- [Vault on Morpho](https://app.morpho.org/vault?vault=0xc1256Ae5FF1cf2719D4937adb3bbCCab2E00A2Ca&network=base)
- [Merkl](https://merkl.xyz)
- [Odos](https://odos.xyz)
- [viem](https://viem.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text, Markdown reports, JSON reports, shell commands, and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, Base USDC and ETH for gas, and a configured wallet source.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
