## Description:

Smart file organizer that helps agents guide local file categorization, renaming, duplicate detection, backup, preview, and undo workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize local folders by file type, rename files, detect duplicates, generate configuration, and undo logged organization actions. It is suited to personal productivity workflows where file operations can be previewed and reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move, delete, rename, or undo operations across real local files.

Mitigation: Run first with --preview on a small, non-sensitive directory, avoid elevated privileges and system or shared folders, and keep separate backups before applying changes.

Risk: Undo behavior depends on trusted operation logs and may act on paths recorded in those logs.

Mitigation: Run undo only against logs created by the same trusted workflow and inspect the planned changes in preview mode before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shianaixuexi-cell/skills/moneyclaw-smart-file-organizer)
- [Artifact README](artifact/README.md)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preview, backup, deduplication, and undo recommendations for local file operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
