## Description:

Manage OpenClaw agent lifecycle operations on a node, including agent creation, Telegram channel binding and pairing, archiving, deletion, dashboard refreshes, and lifecycle logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miniade](https://clawhub.ai/user/miniade)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw nodes use this skill to create or reconfigure Telegram-connected agents, approve pairing, archive before deletion, refresh status dashboards, and maintain lifecycle audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts handle sensitive local agent files and credentials.

Mitigation: Use only with trusted operators and trusted agent IDs; avoid credential inheritance unless the user explicitly approves it.

Risk: Telegram tokens may be exposed when passed on the command line.

Mitigation: Avoid passing real Telegram tokens on the command line; prefer a more private secret-handling path before production use.

Risk: Archive outputs can contain workspace data, status snapshots, or other sensitive operational records.

Mitigation: Restrict archive locations and permissions, and redact or minimize archived status and workspace data.

Risk: Unsafe path and temporary-file practices can affect local files when untrusted identifiers are used.

Mitigation: Patch scripts to validate agent IDs and use private temporary paths created with mktemp before broad deployment.

## Reference(s):

- [OpenClaw Agent Lifecycle Playbook](references/openclaw-agent-lifecycle-playbook.md)
- [ClawHub skill page](https://clawhub.ai/miniade/skills/miniade-agent-lifecycle-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and helper script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct use of the local OpenClaw CLI and produce archive, dashboard, status, and lifecycle log files.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
