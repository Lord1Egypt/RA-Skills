## Description:

Command-line agent skill for creating, trading, swapping, transferring, and inspecting Mint Club V2 bonding curve tokens on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebayaki](https://clawhub.ai/user/sebayaki)

### License/Terms of Use:


## Use Case:

External developers and agent users use this skill to operate the Mint Club CLI for Base blockchain token queries, trades, swaps, token creation, wallet checks, and transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate irreversible financial actions on Base mainnet, including buy, sell, swap, create, and send commands.

Mitigation: Use a dedicated low-balance wallet, inspect every transaction and approval before signing, and revoke allowances after use.

Risk: The skill uses raw wallet private keys through CLI configuration or the PRIVATE_KEY environment variable.

Mitigation: Do not import a primary wallet private key; use a separate wallet created for this workflow.

Risk: The skill depends on a globally installed npm CLI package for wallet and token operations.

Mitigation: Verify the npm package and version before installation or execution.

## Reference(s):

- [Mint Club V2 Docs](https://docs.mint.club)
- [mint.club-cli npm package](https://www.npmjs.com/package/mint.club-cli)
- [Mint Club Community](https://onchat.sebayaki.com/mintclub)
- [ClawHub Skill Page](https://clawhub.ai/sebayaki/skills/mintclub)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CLI command guidance for real Base mainnet wallet and token operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
