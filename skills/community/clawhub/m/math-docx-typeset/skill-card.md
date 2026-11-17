## Description:

Converts academic manuscripts and derivations containing LaTeX formulas into DOCX files with native editable Word OMML equations, with an optional image comparison attachment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, students, and other document authors use this skill to turn academic drafts, derivations, or transcribed formula content into editable Word DOCX documents while preserving mathematical notation for local Word or WPS review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential manuscripts, screenshots, or formulas may be routed to external OCR or public rendering services without clear consent controls.

Mitigation: Use local or approved processing paths for confidential content, and only use screenshot OCR or public KaTeX-style rendering after explicit user approval.

Risk: The documented dependency installation uses unpinned Python packages.

Mitigation: Run the skill in a sandboxed environment with reviewed, pinned dependency versions before using it on important documents.

## Reference(s):

- [Formula Rules](references/formula-rules.md)
- [Font Strategy](references/font-strategy.md)
- [Symbol Table](references/symbol-table.md)
- [Transcription](references/transcription.md)
- [latex2mathml](https://github.com/roniemartinez/latex2mathml)
- [mathml2omml](https://github.com/amedama41/mathml2omml)
- [python-docx](https://github.com/python-openxml/python-docx)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [Office Open XML Math Namespace](http://schemas.openxmlformats.org/officeDocument/2006/math)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Guidance]

**Output Format:** [DOCX files with Markdown or text status messages and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary DOCX output uses native editable OMML equations; optional image-variant DOCX may contain PNG formula previews for comparison.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
