## Description:

Interact with Joplin notes via CLI for reading, creating, editing, managing todos, WebDAV sync, and kanban-formatted notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davek-dev](https://clawhub.ai/user/davek-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent operate the Joplin CLI for note, notebook, todo, sync, import/export, and kanban-note workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Joplin notes may contain sensitive data, and WebDAV credential commands can expose secrets in shell history or logs.

Mitigation: Review the skill before installing, avoid entering real WebDAV passwords directly in logged shell commands, and use safer credential handling where available.

Risk: The skill includes commands that delete notes or notebooks.

Mitigation: Require explicit user confirmation before deletion, list the target first, and prefer note or notebook IDs over titles.

Risk: Incorrect direct edits to Joplin storage can cause sync conflicts or data loss.

Mitigation: Use the Joplin CLI instead of direct database edits, then sync and verify important changes with `joplin cat` or status commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davek-dev/skills/joplin-cli-skill)
- [Publisher profile](https://clawhub.ai/user/davek-dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destructive Joplin CLI commands and WebDAV credential configuration examples that require explicit user confirmation before use.]

## Skill Version(s):

1.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
