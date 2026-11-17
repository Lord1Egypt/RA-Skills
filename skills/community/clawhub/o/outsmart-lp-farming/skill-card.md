## Description:

Manage LP positions on Solana DEXes to earn swap fees, including workflows for DLMM, DAMM v2, rebalancing, pool creation, and fee claiming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outsmartchad](https://clawhub.ai/user/outsmartchad)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan and execute Solana on-chain LP farming actions with the outsmart CLI, including adding, monitoring, rebalancing, claiming fees, and exiting positions. It is not for lending, staking, or centralized-exchange market making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real crypto funds through LP add, remove, rebalance, pool creation, and fee-claiming workflows.

Mitigation: Use only a dedicated low-value wallet, preview every transaction with a signer, and confirm the pool, token mint, amounts, fee settings, and DEX before approving.

Risk: The required outsmart CLI package is unpinned in the release evidence.

Mitigation: Verify the exact CLI package and version before installing, and avoid auto-updating the CLI in production or high-value wallet contexts.

Risk: The skill requires PRIVATE_KEY and MAINNET_ENDPOINT environment variables.

Mitigation: Do not expose a wallet containing unrelated assets or authorities; use an isolated runtime session and avoid logging or sharing private-key material.

## Reference(s):

- [Outsmart LP Farming ClawHub page](https://clawhub.ai/outsmartchad/skills/outsmart-lp-farming)
- [Outsmart CLI homepage](https://github.com/outsmartchad/outsmart-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the outsmart CLI plus PRIVATE_KEY and MAINNET_ENDPOINT environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
