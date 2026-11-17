## Description:

OpenStatus CLI helps agents manage status-page incidents, status reports, maintenance windows, monitor configuration, and subscriber notifications from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openstatus](https://clawhub.ai/user/openstatus)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, SREs, and developers use this skill to create, update, resolve, and inspect OpenStatus incidents and maintenance windows. It also guides monitor configuration through openstatus.yaml examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands using --notify can send messages to status-page subscribers.

Mitigation: Require explicit user approval before any command that includes --notify.

Risk: Delete commands can remove OpenStatus incident or maintenance records, and -y skips confirmation.

Mitigation: Confirm the target record ID and user intent before delete commands; avoid -y unless the user explicitly approves it.

Risk: Monitor headers and bodies can contain secrets, and public monitors may expose internal endpoints.

Mitigation: Avoid broad production secrets in monitor configuration, and keep internal monitors private unless they are intended for public status pages.

## Reference(s):

- [Monitor Configuration Reference](references/monitor-config.md)
- [OpenStatus Official Website](https://www.openstatus.dev)
- [OpenStatus CLI Repository](https://github.com/openstatusHQ/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenStatus CLI commands and openstatus.yaml snippets; OpenStatus authentication is required before account changes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
