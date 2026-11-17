## Description:

Operates the Informat platform for applications, tables, workflows, automations, scripts, APIs, dashboards, records, listeners, schedules, and generated files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[informat365](https://clawhub.ai/user/informat365)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform operators use this skill to inspect, configure, and automate Informat workspaces, including app structures, data tables, workflows, dashboards, scripts, APIs, schedules, and user-facing records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad administrative and mutating access to Informat deployments.

Mitigation: Install only in trusted Informat deployments, use a least-privilege revocable agent token, and require explicit user approval before destructive or privileged operations.

Risk: The helper can transmit the agent token over plaintext HTTP if INFORMAT_HOST is not HTTPS.

Mitigation: Require INFORMAT_HOST to use HTTPS before deployment.

Risk: Local environment files can expose secrets if used for agent credentials.

Mitigation: Avoid scripts/.env for secrets and rely on trusted runtime secret injection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/informat365/skills/informat)
- [Informat skill instructions](artifact/SKILL.md)
- [Informat application documentation](artifact/references/doc/markdown/informat.app.md)
- [Informat table documentation](artifact/references/doc/markdown/informat.table.md)
- [Informat workflow documentation](artifact/references/doc/markdown/informat.bpmn.md)
- [Informat dashboard UI preset documentation](artifact/references/doc/markdown/informat.dashboard.uipreset.md)
- [Informat script documentation](artifact/references/doc/markdown/informat.script.md)
- [Informat expression documentation](artifact/references/doc/markdown/informat.expression.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured command guidance with JSON parameter files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Informat platform methods that read, create, update, delete, publish, execute scripts, manage users or roles, configure listeners, and schedule tasks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
