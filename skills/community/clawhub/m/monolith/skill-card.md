## Description:

Secure crypto wallet for AI agents with hardware-isolated keys, an ERC-4337 smart wallet, on-chain spending caps, and a default-deny policy engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slaviquee](https://clawhub.ai/user/slaviquee)

### License/Terms of Use:


## Use Case:

External users, developers, and agent operators use this skill to let an agent prepare wallet actions such as transfers, swaps, balance checks, setup checks, policy changes, allowlist updates, audit log review, and emergency freezes through Monolith's local macOS daemon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on externally downloaded macOS components with persistent wallet authority.

Mitigation: Verify release signatures and hashes independently before installation and review what the daemon can authorize.

Risk: Fund-moving swap actions may depend on remote swap data and require careful validation.

Mitigation: Avoid large-value swaps until the external binaries and swap validation path have been independently audited.

Risk: Approval codes entered through command-line flows can expose sensitive authorization steps.

Mitigation: Use small test transactions first and avoid command-line approval codes for high-value or unfamiliar transactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slaviquee/skills/monolith)
- [Publisher profile](https://clawhub.ai/user/slaviquee)
- [Homepage](https://github.com/slaviquee/monolith)
- [Skill source](https://github.com/slaviquee/monolith/tree/main/skill)
- [Monolith daemon package](https://github.com/slaviquee/monolith/releases/download/v0.1.5/MonolithDaemon-v0.1.5.pkg)
- [Monolith companion app](https://github.com/slaviquee/monolith/releases/download/v0.1.3/MonolithCompanion.app.zip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with command outputs and JSON policy input where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, a local MonolithDaemon binary, and a funded wallet for fund-moving actions.]

## Skill Version(s):

0.1.10 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
