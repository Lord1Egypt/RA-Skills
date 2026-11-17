## Description:

Routes user prompts that name supported DeFi DApps or protocol-native tokens to the matching third-party plugin, installs it when needed, and forwards the original request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover and launch OKX DeFi protocol plugins for swaps, staking, lending, prediction-market bets, perpetuals, and related actions when the prompt identifies a supported DApp or token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The router can install and activate third-party DeFi plugins globally from mutable online sources.

Mitigation: Ask before installing, pin the installer and plugin revision, prefer per-project installation where available, and provide an uninstall path.

Risk: The skill forwards user requests to downstream plugins that may handle trades, bets, transfers, or other write actions.

Mitigation: Review downstream plugin behavior before use and require explicit user confirmation before any trade, bet, transfer, or other write operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ok-james-01/skills/okx-dapp-discovery)
- [OKX Web3](https://web3.okx.com)
- [OKX plugin-store catalog endpoint](https://api.github.com/repos/okx/plugin-store/contents/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes to downstream plugins; downstream plugins own protocol-specific trade, bet, or transfer behavior.]

## Skill Version(s):

3.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
