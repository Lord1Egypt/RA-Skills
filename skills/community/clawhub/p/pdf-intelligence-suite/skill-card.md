## Description:

PDF Intelligence Suite helps agents and developers extract text and tables, run OCR, convert PDFs, manipulate pages, and apply basic PDF security operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to automate PDF document analysis and transformation workflows, including text extraction, table export, OCR, conversion to office or image formats, and page-level PDF operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe export and file-handling behavior may affect local files or produce risky downstream artifacts.

Mitigation: Run the skill in a dedicated working directory, review generated files before use, and avoid running the example script near important documents.

Risk: Generated HTML and spreadsheet files from untrusted PDFs may carry unsafe or misleading content.

Mitigation: Process only authorized PDFs and sanitize or inspect exported HTML, CSV, and spreadsheet files before opening or sharing them.

Risk: PDF copy or print restrictions may not be reliably enforced by the current permission-restriction API.

Mitigation: Treat permission settings as advisory and use external document controls when enforceable copy or print limits are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/pdf-intelligence-suite)
- [Project Homepage](https://github.com/kaiyuelv/pdf-intelligence-suite)
- [Tesseract OCR Windows Installer Reference](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python code and shell command examples; PDF-derived outputs may include text, CSV, Excel, DOCX, images, and HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python dependencies and external OCR support for Tesseract-based OCR workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
