## Description:

A Mac disk-audit assistant that reviews storage usage and provides prioritized, confirmation-first cleanup recommendations and commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

Mac users and developers use this skill to identify large files and reclaim disk space with a review-first cleanup plan. It reports findings and proposed commands without automatically deleting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some cleanup recommendations can permanently erase project history, logs, or application data.

Mitigation: Start with read-only reports; never treat `.git/objects/` as disposable, and review exact targets and backups before deleting files or Docker volumes.

Risk: The skill includes blanket privileged log-wipe and other destructive cleanup commands, as well as unrelated promotional content.

Mitigation: Avoid blanket privileged log wipes, require explicit confirmation for reviewed deletions, and disregard unrelated promotional material.

## Reference(s):

- [ClawHub release](https://clawhub.ai/guipi888/skills/mac-disk-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with prioritized cleanup findings and copyable shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reporting; cleanup commands require explicit user review and confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
