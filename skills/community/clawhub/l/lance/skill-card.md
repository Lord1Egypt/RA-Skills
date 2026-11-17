## Description:

Lance is a Web3 bug bounty and protocol security agent for evidence-backed vulnerability discovery and reporting across smart contracts, DeFi protocols, EVM/Solidity, Sui Move, wallet/signature flows, and bridges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaniidev](https://clawhub.ai/user/shaniidev)

### License/Terms of Use:

MIT

## Use Case:

Developers, security researchers, and protocol teams use Lance to audit authorized Web3 targets, reject speculative findings, validate exploitability and economic feasibility, and prepare triage-ready bug bounty reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be implicitly selected for Web3 audit prompts, which may trigger exploit-focused analysis unintentionally.

Mitigation: Disable implicit invocation or install it only in agents and workspaces where Web3 audit behavior is expected.

Risk: The skill is designed for exploitability-focused security analysis and can be misused outside authorized testing.

Mitigation: Use it only with bug bounty scope, explicit written permission, or owned/internal systems.

Risk: GitHub install instructions are unpinned, so installs can drift from the reviewed release.

Mitigation: Install from a reviewed commit or signed release when possible.

## Reference(s):

- [Lance ClawHub skill page](https://clawhub.ai/shaniidev/skills/lance)
- [Publisher profile](https://clawhub.ai/user/shaniidev)
- [Source repository](https://github.com/shaniidev/lance)
- [Publisher GitHub profile](https://github.com/shaniidev)
- [README](README.md)
- [Workflow](references/workflow.md)
- [Web3 Audit Rules](references/audit-rules.md)
- [Exploit Validation](references/exploit-validation.md)
- [Economic Validation](references/economic-validation.md)
- [False-Positive Elimination](references/false-positive-elimination.md)
- [Severity Guide Web3](references/severity-guide-web3.md)
- [Triage Simulation](references/triage-simulation.md)
- [Wallet Trust Boundary](references/wallet-trust-boundary.md)
- [EVM Chain Guide](references/chains/evm.md)
- [Sui Move Chain Guide](references/chains/sui-move.md)
- [Cross-Chain and Bridge Guide](references/chains/cross-chain-bridge.md)
- [Finding schema](assets/templates/finding.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, structured finding JSON, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should pass scope, exploitability, economic feasibility, false-positive, and triage gates; when no finding passes, the skill outputs that no exploitable on-chain vulnerabilities were identified.]

## Skill Version(s):

0.0.1 (source: SKILL.md frontmatter metadata.version and CHANGELOG.md, released 2026-02-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
