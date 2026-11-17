## Description:

Use the official Obsidian CLI for note workflows in a Git-backed vault, including search, read, links/backlinks-style queries, daily-note operations, and lightweight note writes that auto-sync after successful write operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinrowe](https://clawhub.ai/user/darinrowe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and note-taking agents use this skill to query and update an existing Obsidian vault through the official CLI, with Git backup behavior after successful lightweight writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback note writes may target paths outside the intended vault if note names are not validated.

Mitigation: Run under a non-privileged account and validate note paths before use; reject absolute paths and traversal segments.

Risk: The backup script stages all detected Git changes and pushes automatically after writes.

Mitigation: Review the backup script, keep secrets and temporary files out of the vault with .gitignore, and consider requiring confirmation or staging only the changed note before pushing.

Risk: A successful write can still fail to sync, leaving local vault changes unpushed.

Mitigation: Check the reported sync status after each write and resolve failed Git sync before assuming the note is backed up.

## Reference(s):

- [Query vs write](references/query-vs-write.md)
- [Fallback policy](references/fallbacks.md)
- [Workflow surface](references/workflow-surface.md)
- [Environment note](references/environment-note.md)
- [Obsidian official CLI headless companion skill](https://clawhub.ai/DarinRowe/obsidian-official-cli-headless)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional script-mediated workflow output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the command or workflow used, target note or path, whether sync ran, and whether sync succeeded.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
