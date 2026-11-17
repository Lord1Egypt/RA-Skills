## Description:

节点工作工具专业版 helps teams manage multi-node cluster deployment, task scheduling preferences, revenue dashboards, cost accounting, and centralized wallet operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to plan and operate node clusters, configure scheduling preferences, review revenue and cost metrics, and generate cluster workflow commands and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt broad command or file operations for node clusters, wallets, and environment configuration.

Mitigation: Require explicit user confirmation before command execution, .env or API-key access, wallet changes, deployments, auto-restart setup, or persistent monitoring changes.

Risk: Wallet and cluster management workflows can affect funds, credentials, or running infrastructure.

Mitigation: Use least-privilege keys, RBAC-scoped credentials, multisig wallet controls where applicable, and backups for configuration files before changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jinn-node-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, Python, and text blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured status, result, execution log, and error fields for node operations workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
