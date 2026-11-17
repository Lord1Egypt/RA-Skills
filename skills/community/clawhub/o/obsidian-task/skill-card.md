## Description:

Manage Obsidian tasks via obsidian-cli to list, toggle, create, and update tasks from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyd4y](https://clawhub.ai/user/boyd4y)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage task notes in an Obsidian vault from an agent-assisted terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make user-directed edits to task files in an Obsidian vault.

Mitigation: Review file, line, and content arguments before approving update or append commands, and keep vault backups or sync history available for undo.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boyd4y/skills/obsidian-task)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local obsidian command, Obsidian 1.12 or later, a Catalyst license, CLI registration, and a running Obsidian app.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
