## Description:

Launch tokens on Solana launchpads, with guidance for creating coins on PumpFun, Jupiter Studio, Raydium LaunchLab, and Meteora DBC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outsmartchad](https://clawhub.ai/user/outsmartchad)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to plan and execute Solana token launches on launchpads such as PumpFun, Jupiter Studio, Raydium LaunchLab, and Meteora DBC. It is scoped to creating new tokens and post-graduation liquidity actions, not buying existing tokens or farming existing pools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious because it asks an agent to install an unpinned third-party CLI and use a raw mainnet wallet private key for irreversible Solana financial actions.

Mitigation: Use a dedicated low-balance wallet, verify the outsmart CLI package and version before installation, and require full transaction review before signing any mainnet launch, pool, or liquidity command.

Risk: The artifact includes commands for token launches, pool creation, and liquidity actions that can spend funds or alter assets on mainnet.

Mitigation: Confirm launchpad choice, token metadata, wallet, endpoint, amounts, fee settings, and liquidity parameters with the user before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/outsmartchad/skills/outsmart-devving-coins)
- [Publisher profile](https://clawhub.ai/user/outsmartchad)
- [Outsmart CLI homepage](https://github.com/outsmartchad/outsmart-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference the outsmart CLI and the PRIVATE_KEY and MAINNET_ENDPOINT environment variables when command execution is relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
