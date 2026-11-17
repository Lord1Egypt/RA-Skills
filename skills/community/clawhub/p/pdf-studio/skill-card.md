## Description:

Professional PDF document generator for reports, invoices, certificates, portfolios, and other publication-ready PDFs with support for images, tables, charts, tables of contents, headers, footers, and cross-platform fonts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to plan and generate professional PDFs such as business reports, invoices, certificates, resumes, portfolios, academic papers, and forms. It guides document requirements, layout choices, font selection, and local PDF library use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PDF code or commands may be incorrect or unsuitable for the user's environment.

Mitigation: Review generated code before running it and test output locally before using generated PDFs in production workflows.

Risk: PDF generation depends on user-installed Python libraries such as FPDF2, WeasyPrint, or ReportLab.

Mitigation: Install dependencies manually from trusted sources and verify the selected library supports the required document features and fonts.

Risk: Some prompts and templates are Chinese-focused despite broader multilingual claims.

Mitigation: Confirm language, font, and layout requirements for the target audience before finalizing the document.

## Reference(s):

- [PDF Templates](artifact/references/templates.md)
- [ClawHub skill page](https://clawhub.ai/tobewin/skills/pdf-studio)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local PDF-generation code or commands; generated code should be reviewed before execution and dependencies should be installed manually from trusted sources.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
