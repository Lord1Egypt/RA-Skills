## Description:

Trade tokens on Solana via the outsmart CLI: buy, sell, quote, find pools, add/remove liquidity, claim fees, snipe, create pools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outsmartchad](https://clawhub.ai/user/outsmartchad)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to ask an agent for Solana DEX trading and liquidity-management commands with the outsmart CLI. It is scoped to on-chain Solana DEX activity, not Ethereum/EVM trading, centralized exchange orders, cross-chain bridges, or historical charting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can move real funds from a Solana wallet.

Mitigation: Use an isolated environment, a dedicated low-balance wallet, and dry runs before any funded transaction.

Risk: A raw private key is required and may be stored in ~/.outsmart/config.env.

Mitigation: Treat the config file as a highly sensitive secret, restrict file access, and avoid using a primary wallet.

Risk: The release depends on an unpinned third-party npm package.

Mitigation: Install only after independently trusting the outsmart package and reviewing the exact package version to be used.

Risk: Incorrect token mints, pools, destinations, amounts, or RPC endpoints can cause unintended transactions.

Mitigation: Verify all transaction inputs before execution and start with small test trades for unfamiliar assets.

## Reference(s):

- [Outsmart DEX Trading on ClawHub](https://clawhub.ai/outsmartchad/skills/outsmart-dex-trading)
- [Outsmart CLI homepage](https://github.com/outsmartchad/outsmart-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may execute real Solana transactions when run outside dry-run mode; review wallet, token, pool, destination, amount, and endpoint details before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
