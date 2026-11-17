## Description:

Scan, deduplicate, and organize files in a directory by generating a dry-run cleanup plan before any optional file moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan folders such as Downloads or Desktop, identify duplicate files, create file inventories, generate dry-run organization plans, and optionally move files after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Execute mode can move or overwrite files beyond the intended folder if run from a crafted scan file or with non-interactive confirmation.

Mitigation: Use dry-run first, inspect the complete JSON plan, avoid plans from untrusted scan files, and use --execute --yes only after checking backups and destination conflicts.

## Reference(s):

- [File category mappings](artifact/references/categories.md)
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/skills/nai-file-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON inventories and move plans, and markdown manifest reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; optional execution moves files and should be reviewed before confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
