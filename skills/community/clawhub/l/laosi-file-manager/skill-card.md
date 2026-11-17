## Description:

Windows文件管理器 helps an agent create, copy, move, delete, search, rename, compare, and organize Windows files and folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to ask an agent to organize Windows folders, perform batch file operations, search file trees, inspect file attributes, and produce operation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete, overwrite, recursive folder removal, and batch operations can permanently remove user files.

Mitigation: Require explicit confirmation, keep backups, review the proposed operation list, and scope execution to a known workspace before making changes.

Risk: The install command includes standard-library modules and should not be followed as written without review.

Mitigation: Review dependency needs before installation and only install packages from trusted sources when a real external dependency is required.

Risk: The documented path blacklist is narrow and environment-specific.

Mitigation: Use allow-list based path scoping and manually review operations that touch system, desktop, application data, or shared directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-file-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-operation examples and operation-report text; actions should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
