## Description:

Automates common local office tasks including Excel consolidation, Word text replacement, PDF merging, and batch file renaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoheizp](https://clawhub.ai/user/xiaoheizp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations staff use this skill to automate local office workflows such as consolidating spreadsheets, replacing text across Word documents, merging PDFs, and renaming batches of files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk local file operations can rename files or modify Word documents in place.

Mitigation: Run the skill only on backed-up copies, test patterns on sample folders first, and scope inputs to the smallest practical directory.

Risk: Broad replacements or rename patterns can affect more files than intended because safeguards and bounds are limited.

Mitigation: Review input paths and replacement or rename values before execution, and inspect generated reports and changed files before relying on the results.

Risk: The advertised email-send capability is unsupported in the inspected code.

Mitigation: Treat email sending as unavailable unless a separate implementation is provided and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoheizp/skills/ke-office-automation)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [CLI text plus generated local files and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; optional pandas/openpyxl, pypdf, and python-docx packages are needed for full document processing.]

## Skill Version(s):

1.1.0 (source: server release metadata; SKILL.md frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
