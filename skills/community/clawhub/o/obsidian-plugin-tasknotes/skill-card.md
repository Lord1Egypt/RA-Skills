## Description:

Manage tasks in Obsidian via TaskNotes plugin API. Use when user wants to create tasks, list tasks, query by status or project, update task status, delete tasks, or check what they need to do.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benoitjadinon](https://clawhub.ai/user/benoitjadinon)

### License/Terms of Use:


## Use Case:

External users and developers who manage tasks in Obsidian use this skill to list, create, update, delete, and review TaskNotes items through the local TaskNotes HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete Obsidian TaskNotes data.

Mitigation: Require explicit user confirmation before update or delete actions, especially when task identifiers are ambiguous.

Risk: Sensitive task content or the TaskNotes API token could be exposed if local environment settings are tampered with.

Mitigation: Use a trusted vault .env file, keep TASKNOTES_API_PORT as a simple numeric localhost port, and use a limited TaskNotes token when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benoitjadinon/skills/obsidian-plugin-tasknotes)
- [Publisher profile](https://clawhub.ai/user/benoitjadinon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON or table-formatted CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Obsidian TaskNotes HTTP API access and optional TASKNOTES_API_KEY/TASKNOTES_API_PORT environment configuration.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
