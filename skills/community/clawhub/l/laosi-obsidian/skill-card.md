## Description:

Obsidian笔记助手 helps agents create, search, and organize Markdown notes in a local Obsidian vault, including bidirectional links, tags, graph export, and daily note automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent manage a local Obsidian vault: create notes and daily notes, search Markdown content, audit tags, find backlinks, and export graph data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates on local Markdown notes and can create, overwrite, export, or bulk-scan vault content if the agent executes generated commands.

Mitigation: Set the vault path deliberately, keep backups or version control for notes, and require confirmation before file writes, exports, and bulk scans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-obsidian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Python, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Markdown files in a user-selected local Obsidian vault when commands are executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
