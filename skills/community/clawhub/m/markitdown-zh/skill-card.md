## Description:

使用微软 markitdown 库将多种文档格式（PDF、DOCX、PPTX、XLSX、XLS、CSV、JSON、TXT、EPUB、HTML等）转换为 Markdown，并支持批量转换和图片提取。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapleshadow](https://clawhub.ai/user/mapleshadow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to convert individual files or folders of PDFs, Office documents, spreadsheets, text files, ebooks, and HTML into Markdown. It can also help extract document images when the underlying MarkItDown conversion result exposes them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing MarkItDown with optional dependencies or system packages may add software the user has not reviewed.

Mitigation: Use a virtual environment or pipx under the user account, pin dependency versions where possible, and review package installation commands before running them.

Risk: Batch conversion recursively reads files from the input directory.

Mitigation: Point batch conversion only at folders containing documents intended for conversion.

Risk: Converted Markdown and extracted images can contain sensitive content from the source documents.

Mitigation: Write outputs to an approved location and handle generated files according to the same data controls as the source documents.

## Reference(s):

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- [ClawHub skill page](https://clawhub.ai/mapleshadow/skills/markitdown-zh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts produce Markdown files and extracted image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+ and the MarkItDown package; optional system dependencies may be needed for some formats.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
