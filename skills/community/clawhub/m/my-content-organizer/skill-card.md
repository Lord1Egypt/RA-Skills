## Description:

Organize workspace files by type, extension, and date. Use when: workspace is cluttered, need to sort downloads, clean up screenshots, organize media files, or prepare files for archival/backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and general workspace users can use this skill to scan a cluttered directory, create category folders, preview file moves, and organize top-level files by extension.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly move or overwrite files when executed in the current directory.

Mitigation: Run the dry run first, review every proposed move, and execute only in a directory explicitly chosen for organization.

Risk: The hidden-file safety note is inaccurate for the provided find command.

Mitigation: Avoid folders containing dotfiles or revise the command to exclude hidden files before executing moves.

Risk: Existing category folders or important workspace roots can make file moves hard to review or undo.

Mitigation: Avoid project roots, home directories, and folders with important existing category folders unless the command is revised to prevent overwrites and reject unsafe paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/my-content-organizer)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for scanning, dry-run review, file moves, and verification; requires standard Unix tools mkdir, mv, and find.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
