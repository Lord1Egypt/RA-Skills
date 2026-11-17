## Description:

Edit and validate OpenClaw Gateway config (openclaw.json / JSON5), covering gateway, agents, channels, models, auth, tools, commands, session, hooks, secrets, acp, messages, plugins, skills, and $include settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqbjqtd](https://clawhub.ai/user/aqbjqtd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to edit, validate, troubleshoot, and migrate OpenClaw Gateway configuration without introducing schema errors or weakening security policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a protected-path workaround for sensitive OpenClaw settings that bypasses online config.patch controls.

Mitigation: Use the workaround only for intentional privileged security changes after explicit review, with a backup and rollback plan.

Risk: Server security evidence flags the backup and restore scripts for unsafe temp-file and deletion handling.

Mitigation: Review and harden those scripts before running them on a real gateway or against live configuration files.

Risk: Configuration examples and operational guidance can expose credentials if copied into logs, chat, or world-readable files.

Mitigation: Keep secrets in managed secret providers or tightly permissioned environment files, and do not paste secret values into logs or chat transcripts.

## Reference(s):

- [OpenClaw Gateway Configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Config CLI](https://docs.openclaw.ai/cli/config)
- [OpenClaw Security CLI](https://docs.openclaw.ai/cli/security)
- [OpenClaw Models](https://docs.openclaw.ai/gateway/models)
- [OpenClaw Agents](https://docs.openclaw.ai/gateway/agents)
- [OpenClaw Tools](https://docs.openclaw.ai/gateway/tools)
- [Channels Configuration](references/channels-config.md)
- [Common Configuration Errors](references/common-errors.md)
- [Complex Configuration Operations](references/complex-operations.md)
- [OpenClaw Config Field Index](references/openclaw-config-fields.md)
- [Schema Sources](references/schema-sources.md)
- [Version Migration](references/version-migration.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or JSON5 configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose configuration file edits, gateway config.patch payloads, validation commands, backup and restore commands, and troubleshooting steps.]

## Skill Version(s):

1.3.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
