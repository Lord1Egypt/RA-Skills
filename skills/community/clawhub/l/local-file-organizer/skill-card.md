## Description:

本地文件整理虾 organizes local files by category, detects duplicates, and guides consistent renaming and archiving workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to preview and run local directory organization for downloads, desktops, project archives, photos, and documents. Use dry-run mode first and work on test or backed-up folders because the skill can move files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-moving behavior can reorganize local files unexpectedly or outside the intended target.

Mitigation: Run with --dry-run first, use a separate target directory, and manually review the planned moves before execution.

Risk: Running the skill on broad locations can affect many unrelated files.

Mitigation: Start with test folders or backed-up data and avoid broad paths such as a home directory or full project tree.

Risk: Custom rules can place files into unintended folders if category names are unsafe or unreviewed.

Mitigation: Use --rules only with trusted JSON files and simple folder names.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/local-file-organizer)
- [Classification Rules](references/classification-rules.md)
- [Duplicate Detection](references/duplicate-detection.md)
- [Naming Conventions](references/naming-conventions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a JSON organization report when the bundled script is run outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
