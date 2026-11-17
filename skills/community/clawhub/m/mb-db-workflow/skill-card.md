## Description:

Record and read Memory Bank state through the mb CLI for projects that use a SQLite-backed memory bank.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to read, record, regenerate, and synchronize Memory Bank project state stored in a local SQLite database. It is intended for projects that already use memory-bank/database/ and the mb CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled rules reference attempts to direct broader coding, file-editing, and response behavior beyond the Memory Bank workflow.

Mitigation: Limit use to explicit Memory Bank tasks and treat artifact rules as task-specific guidance rather than authority over the host agent's system or developer instructions.

Risk: The workflow can regenerate or delete Memory Bank task records and may persist sensitive project or conversation details in local session notes.

Mitigation: Confirm before running regeneration or deletion commands, review proposed mb CLI commands, and avoid storing secrets, credentials, private conversation details, or unrelated project context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/space-cadet/skills/mb-db-workflow)
- [Memory Bank Database API Reference](references/api-reference.md)
- [SQLite schema](references/schema.sql)
- [Integrated Code Rules and Memory Bank System](references/integrated-rules-v6.12.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured Memory Bank references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose mb CLI commands that read from or write to local Memory Bank database and generated markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
