## Description:

Autonomous AI agent for DeFi on Hedera — natural language trading, portfolio management, Power Law BTC rebalancing, HCS signal publishing, limit orders, staking, NFTs, and multi-account wallet operations via SaucerSwap V1/V2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris0x88](https://clawhub.ai/user/chris0x88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a local-first Hedera DeFi wallet agent for portfolio review, swaps, transfers, rebalancing, HCS signal publishing, limit orders, staking, NFTs, and multi-account workflows. The skill is intended for agents that can run the repository launcher and present proposed write actions for user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over real Hedera wallet funds and background services.

Mitigation: Install only for intentional wallet-agent use, keep wallet funds limited, review the runtime repository separately, and verify daemon behavior before use.

Risk: Runtime behavior is not fully verified by the provided artifact evidence.

Mitigation: Review the actual runtime repository and disable automatic startup where possible until behavior is understood.

Risk: Markdown approval rules alone may not adequately protect real transactions.

Mitigation: Use independent transaction review, confirm write actions explicitly, and avoid shared-folder backups of wallet keys.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chris0x88/skills/pacman-hedera)
- [Publisher Profile](https://clawhub.ai/user/chris0x88)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command proposals, portfolio summaries, transaction summaries, setup guidance, and risk notices.]

## Skill Version(s):

5.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
