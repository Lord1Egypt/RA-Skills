## Description:

Research crypto and meme tokens by address using GMGN API data for price, liquidity, holders, traders, smart money and KOL positions, and security signals across Solana, BNB Smart Chain, Base, and Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmgnai](https://clawhub.ai/user/gmgnai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to perform token due diligence, including market, liquidity, holder, trader, and security analysis before making crypto trading or monitoring decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can install a global npm dependency.

Mitigation: Preinstall and review a pinned gmgn-cli version before enabling the skill.

Risk: The skill handles GMGN API requests and persistent local API-key storage.

Mitigation: Configure credentials through a trusted secret store or manual setup outside the agent when possible.

Risk: First-time setup can create key material on disk.

Mitigation: Review generated key files and remove temporary key material after setup.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gmgnai/skills/gmgn-token)
- [GMGN API key setup](https://gmgn.ai/ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured token analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw JSON guidance when users request machine-readable GMGN CLI output.]

## Skill Version(s):

1.4.6 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
