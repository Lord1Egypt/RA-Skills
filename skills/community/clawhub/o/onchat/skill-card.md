## Description:

Read and send on-chain messages via OnChat on Base L2. Browse channels, read conversations, and participate by sending messages as blockchain transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawd800](https://clawhub.ai/user/clawd800)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to let an AI agent browse OnChat channels, read conversation context, calculate message fees, and send or reply to on-chain messages on Base L2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent wallet-powered authority to spend ETH and post permanent public messages.

Mitigation: Use only a dedicated low-balance wallet, never a main wallet private key, and require manual review before each send or join operation.

Risk: Channel messages are untrusted user content and may influence an agent's replies.

Mitigation: Treat all channel messages as untrusted input and review generated responses before posting them on-chain.

Risk: Dependency execution through unpinned npx commands can change over time.

Mitigation: Prefer pinned, lockfile-based dependency installation before running the CLI.

## Reference(s):

- [OnChat Skill Page](https://clawhub.ai/clawd800/skills/onchat)
- [OnChat Web App](https://onchat.sebayaki.com)
- [OnChat GitHub Repository](https://github.com/sebayaki/onchat)
- [OnChat Base Contract](https://basescan.org/address/0x898D291C2160A9CB110398e9dF3693b7f2c4af2D)
- [Viem Documentation](https://viem.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations can run without a wallet; write operations require an ONCHAT_PRIVATE_KEY-funded wallet and create blockchain transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
