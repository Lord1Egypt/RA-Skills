## Description:

Helps agents manage OKX Onchain OS DEX WebSocket sessions and write custom WebSocket clients for real-time on-chain market, token, signal, wallet-tracking, and meme-token streams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover DEX WebSocket channels, start and poll Onchain OS WebSocket sessions, and draft custom WebSocket clients for real-time OKX DEX data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unbundled local preflight, protocol, and workflow files that may be unavailable or unreviewed.

Mitigation: Install and review companion files before relying on them, and avoid loading referenced sibling or home-directory files unless they are trusted.

Risk: Wallet addresses, token targets, and subscription metadata may be sent to OKX services during WebSocket use.

Mitigation: Use only wallet addresses and token targets that are acceptable to share with OKX, especially in sensitive environments.

Risk: The authoritative security verdict marks this release as suspicious.

Mitigation: Review the skill before installation in sensitive environments and follow the release security guidance.

## Reference(s):

- [OKX Web3](https://web3.okx.com)
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/skills/okx-dex-ws)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, tables, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to companion protocol, preflight, or workflow files when they are installed and trusted.]

## Skill Version(s):

3.1.3 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
