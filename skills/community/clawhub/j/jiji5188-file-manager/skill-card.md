## Description:

Jiji5188 File Manager helps agents organize local files, batch rename files, detect duplicates, and synchronize directories with preview-first Python utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiji5188](https://clawhub.ai/user/jiji5188)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and end users can use this skill to plan and run local file organization, batch renaming, duplicate cleanup, and one-way directory synchronization workflows. It is suited to file-management tasks where previews, confirmations, and backup discipline are important.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file-management commands can move, rename, overwrite, or delete files outside the user's apparent intent in edge cases.

Mitigation: Review proposed commands before execution, test on disposable directories first, and keep independent backups of important data.

Risk: The security guidance flags sync path-overlap and rename destination-containment issues.

Mitigation: Avoid --delete, --execute, --move, --no-confirm, and scheduled automation until those issues are fixed.

## Reference(s):

- [File Management Best Practices](references/best_practices.md)
- [ClawHub Skill Page](https://clawhub.ai/jiji5188/skills/jiji5188-file-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local file operations; scripts default to previews unless execution flags are supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
