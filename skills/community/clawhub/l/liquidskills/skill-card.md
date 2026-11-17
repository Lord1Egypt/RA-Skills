## Description:

Liquidskills is a Hyperliquid development knowledge base for AI agents covering architecture, APIs, wallets, security, testing, deployment, frontend UX, contract addresses, and production review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudzombie](https://clawhub.ai/user/cloudzombie)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to plan, build, test, review, and deploy Hyperliquid dApps and HyperCore/HyperEVM integrations. It routes agents to topic-specific guidance for architecture, APIs, wallets, tooling, security, QA, and audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting HYPE bridge guidance could lead to incorrect wallet, bridge, contract, or UI flows.

Mitigation: Review and correct bridge instructions against current official Hyperliquid documentation before using them.

Risk: Remote installers and package installs can expose a development environment to supply-chain or credential risk.

Mitigation: Run installers only in a clean development environment without production wallet keys or sensitive credentials.

Risk: Transaction and fund-transfer examples may affect real assets if used directly on mainnet.

Mitigation: Test all transaction flows on testnet before using mainnet.

## Reference(s):

- [ClawHub Liquidskills Release](https://clawhub.ai/cloudzombie/skills/liquidskills)
- [Hyperliquid Documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/)
- [Hyperliquid Python SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)
- [Hyperliquid TypeScript SDK](https://github.com/nktkas/hyperliquid)
- [HyperEVM Explorer](https://explorer.hyperliquid.xyz)
- [Hyperliquid Mainnet API](https://api.hyperliquid.xyz)
- [Hyperliquid Testnet API](https://api.hyperliquid-testnet.xyz)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Topic-organized guidance across multiple skill files]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
