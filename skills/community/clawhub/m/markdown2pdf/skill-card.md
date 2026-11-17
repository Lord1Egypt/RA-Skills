## Description:

Convert Markdown files to PDF or PNG with customizable professional themes and colored emoji support via CLI or API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and analysts use this skill to turn Markdown reports, documentation, presentations, and business materials into styled PDF or PNG outputs. It supports command-line and Python API workflows with themes, custom CSS, page sizing, margins, and emoji replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown may become unsanitized HTML that is rendered through wkhtmltopdf.

Mitigation: Use the skill only with trusted Markdown, review the converter and dependencies before installation, and prefer a sandboxed environment for wkhtmltopdf.

Risk: User-controlled output names or paths may write outside the intended output folder.

Mitigation: Keep outputs in a dedicated folder and validate or constrain filenames and output paths before exposing the skill to untrusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leohuang8688/skills/markdown2pdf)
- [markdown package](https://pypi.org/project/markdown/)
- [pdfkit package](https://pypi.org/project/pdfkit/)
- [imgkit package](https://pypi.org/project/imgkit/)
- [wkhtmltopdf](https://wkhtmltopdf.org/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code]

**Output Format:** [PDF and PNG files generated from Markdown, with Markdown usage guidance and Python or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python dependencies and wkhtmltopdf; supports themes, custom CSS, page size, margins, PNG width, and output directory selection.]

## Skill Version(s):

2.1.2 (source: server release metadata; artifact pyproject.toml and CHANGELOG.md list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
