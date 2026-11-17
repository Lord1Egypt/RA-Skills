## Description:

Extract structured data from PDF invoices and documents. Handles scanned PDFs (OCR) and digital PDFs. Outputs clean CSV/Excel with vendor, invoice number, dates, line items, totals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tktk-ai](https://clawhub.ai/user/tktk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to extract invoice fields and line items from digital or scanned PDF invoices into structured files for review, reconciliation, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation recommends system-level dependency installation, which can modify the host Python environment.

Mitigation: Install dependencies in an isolated virtual environment, avoid --break-system-packages, and review or pin dependencies before use.

Risk: Generated CSV, JSON, or spreadsheet-ready files may contain sensitive untrusted invoice content.

Mitigation: Treat generated files as sensitive, sanitize spreadsheet cells, and open CSV output with formula execution disabled before sharing or importing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tktk-ai/skills/pdf-invoice-parser)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated CSV, JSON, or TSV invoice data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain sensitive invoice data and should be reviewed before spreadsheet import or sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
