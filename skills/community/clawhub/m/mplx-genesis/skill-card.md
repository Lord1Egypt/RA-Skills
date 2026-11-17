## Description:

Launch tokens on Solana using Metaplex Genesis protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockiosaurus](https://clawhub.ai/user/blockiosaurus)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan and execute Solana token launches with Metaplex Genesis, including LaunchPool distribution, unlocked allocations, Raydium liquidity graduation, and wallet setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that spend SOL and publish irreversible on-chain token launch state.

Mitigation: Require explicit user confirmation before creating or finalizing a launch, and verify the active wallet address and Solana network before every transaction.

Risk: Use with a real Solana keypair can expose funds if the wrong wallet, excessive balance, or leaked keypair file is used.

Mitigation: Use a dedicated low-balance wallet and keep the keypair path and file contents out of chat, logs, and shared artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockiosaurus/skills/mplx-genesis)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown guidance with tool names, configuration values, and command-oriented steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet setup guidance, token launch parameters, allocation splits, timing, and status-check instructions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
