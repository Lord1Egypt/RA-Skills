## Description:

Operate the GlueX Solana protocol to register profiles, listen to bounties, claim tasks, approve rewards, and map social graph connections directly from the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-chen2050](https://clawhub.ai/user/ai-chen2050)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interact with the GlueX Solana protocol from a local CLI, including profile registration, bounty publishing, bounty claiming, approval, reward release, and event listening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the default local Solana keypair and can submit transaction-capable commands.

Mitigation: Use an isolated, low-value Devnet-only wallet and treat publish, claim, and approve commands as state-changing transactions.

Risk: The npm install path introduces dependency risk for a transaction-capable tool.

Mitigation: Review package-lock changes and dependencies before installation, and avoid exposing funded wallets during npm install.

## Reference(s):

- [GlueX homepage](https://github.com/ai-chen2050/gluex)
- [GlueX website](https://ai-chen2050.github.io/gluex)
- [ClawHub skill page](https://clawhub.ai/ai-chen2050/skills/glue-x)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, npx, a local Solana keypair, and the GlueX IDL built in the expected project path.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
