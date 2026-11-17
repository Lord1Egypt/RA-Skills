## Description:

Bidirectional conversion between Word (.docx), Markdown, and related document formats using pandoc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mo-yuhua](https://clawhub.ai/user/mo-yuhua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-focused agents use this skill to read, write, edit, and convert Word, Markdown, PDF, text, HTML, and EPUB documents through pandoc-based shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says some scripts can be tricked into running unintended commands or modifying files more broadly than users may expect.

Mitigation: Review the shell scripts before installation, use document copies, and avoid untrusted replacement text or conversion option values.

Risk: Document conversions may lose complex styling, headers and footers, page breaks, comments, revisions, macros, or complex table structure.

Mitigation: Keep original files, inspect converted outputs before relying on them, and use reference documents or media extraction options when format preservation matters.

## Reference(s):

- [Supported Formats](references/supported-formats.md)
- [Pandoc Documentation](https://pandoc.org/)
- [Pandoc User Guide](https://pandoc.org/MANUAL.html)
- [LibreOffice Documentation](https://www.libreoffice.org/)
- [ClawHub Skill Page](https://clawhub.ai/mo-yuhua/skills/pandoc-docx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown, plain text, document files, and concise shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converted output depends on installed document tools such as pandoc, LibreOffice, poppler-utils, and TeX.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
