## Description:

Converts PDF documents into Word DOCX files while attempting to preserve fonts, font sizes, paragraph spacing, alignment, text styling, tables, and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yechao1995](https://clawhub.ai/user/yechao1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document operations teams can use this skill to convert PDFs or batches of PDFs into editable DOCX files when retained formatting is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted image files may briefly appear or remain in the working directory if conversion fails.

Mitigation: Run conversions in a private working directory and remove temporary image files after failures, especially when handling confidential PDFs.

Risk: Converted DOCX files may not preserve formatting as precisely as advertised, particularly for complex layouts or PDFs that need OCR.

Mitigation: Review generated Word documents before relying on them and use specialized OCR or layout tools for scanned or complex PDFs.

Risk: Dependency or import issues may prevent reliable conversion in some environments.

Mitigation: Install and test required dependencies in an isolated environment before using the skill for sensitive or production work.

## Reference(s):

- [PDF转Word格式参考](references/format_reference.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [DOCX files and Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file conversion, batch folder conversion, and selected page ranges.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
