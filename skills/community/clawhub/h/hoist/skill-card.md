## Description:

Deploy and manage apps, servers, databases, domains, and environment variables on VPS providers using the Hoist CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g4f4r0](https://clawhub.ai/user/g4f4r0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to guide agents through deploying applications and managing VPS-backed servers, databases, domains, environment variables, logs, and rollback workflows with Hoist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to install and operate an unpinned privileged infrastructure CLI.

Mitigation: Use the skill only in a controlled environment and pin and verify the Hoist CLI version before installation.

Risk: Infrastructure commands may expose secrets such as environment values, API keys, or database URLs in chat or logs.

Mitigation: Avoid printing secret values, prefer stdin or a secrets manager for secret injection, and redact sensitive command output before sharing.

Risk: Commands can modify or destroy live servers, domains, databases, keys, and storage volumes.

Mitigation: Require explicit user confirmation before resource-changing commands and take backups before destructive or volume-deletion operations.

## Reference(s):

- [Hoist GitHub Repository](https://github.com/g4f4r0/hoist)
- [Hoist Skill Page](https://clawhub.ai/g4f4r0/skills/hoist)
- [COMMANDS.md](artifact/COMMANDS.md)
- [DOCKERFILES.md](artifact/DOCKERFILES.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Dockerfile snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing infrastructure instructions that should be reviewed before executing commands against live resources.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
