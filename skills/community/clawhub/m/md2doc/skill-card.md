## Description:

Converts Markdown documents into styled Word, PDF, and HTML outputs with templates, covers, tables of contents, headers, footers, embedded images, formatted tables, and styled code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glory904649854](https://clawhub.ai/user/glory904649854)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert Markdown files into styled .docx, optional PDF, and HTML documents for reports, product requirements, technical notes, and academic content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown with remote image links can trigger network fetching during conversion.

Mitigation: Convert trusted Markdown only or run conversion in a sandboxed or offline environment; avoid untrusted remote image links until remote fetching is reviewed.

Risk: Temporary image cleanup can delete existing data in a .temp_images directory under the output location.

Mitigation: Use a dedicated output directory and ensure .temp_images does not contain important files before running conversion.

## Reference(s):

- [ClawHub skill page: md2doc](https://clawhub.ai/glory904649854/skills/md2doc)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell or Python commands; generated .docx, .pdf, and .html files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written to user-specified or input-adjacent paths; PDF output depends on Microsoft Word or LibreOffice.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
