## Description:

Maintain Obsidian vault core-file notes, topic synthesis notes, folder indexes, and graph links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and Obsidian vault maintainers use this skill to scan document or code workspaces, create generated Markdown support notes, maintain folder and workspace indexes, and identify folders that merit deeper topic synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown notes can persist raw previews from files in the selected vault or workspace.

Mitigation: Run scan and refresh --dry-run first, avoid roots that contain secrets or credentials, and review generated previews before syncing or committing notes.

Risk: Marker-based cleanup can permanently delete generated Markdown files across the selected root.

Mitigation: Use clean-generated --dry-run before deletion and keep backups of generated notes before aggressive cleanup.

Risk: Bulk refreshes may update many Obsidian support notes and indexes at once.

Mitigation: Confirm the vault root and scope before running refresh, then run validate after bulk operations.

## Reference(s):

- [Core File Rules](references/core-file-rules.md)
- [Obsidian Linking Conventions](references/obsidian-linking.md)
- [Topic Synthesis Core Notes](references/topic-synthesis-core-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown notes, JSON scan reports, validation summaries, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update generated Obsidian Markdown files such as .core.md sidecars, folder indexes, workspace indexes, and topic synthesis notes.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
