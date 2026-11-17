## Description:

Professional DOCX/PPTX document editing with tracked changes, formatting preservation, highlights, strikethrough, and Git version control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsukisama9292](https://clawhub.ai/user/tsukisama9292)

### License/Terms of Use:

MIT

## Use Case:

Developers and document authors use this skill to fetch, edit, and review DOCX and PPTX files through JSON-defined replacements, additions, slide edits, and diff reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local files, download documents from URLs or SFTP, and write edited outputs, which can expose or overwrite sensitive user files.

Mitigation: Use trusted document sources, work on copies, review output paths before execution, and avoid using sensitive files unless local handling is acceptable.

Risk: The security summary identifies unsafe SFTP handling and broad document transfer behavior.

Mitigation: Avoid untrusted SFTP or URL inputs until path validation and dependency pinning are fixed.

Risk: The security guidance warns against using the PPTX slide rearrange feature on important presentations.

Mitigation: Test slide edits on disposable copies and manually review important presentations in PowerPoint before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsukisama9292/skills/office-document-editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON edit rules, shell commands, edited DOCX/PPTX files, and Markdown diff reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write edited documents, generated Markdown, diff reports, and local Git commits when the workflow script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
