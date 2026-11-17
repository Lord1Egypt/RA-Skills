## Description:

Finds invoice and itinerary attachments in a configured mailbox, extracts text from invoice PDFs with a tiered PDF/OCR flow, merges related PDFs for A4 printing, and generates a two-sheet expense workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leahlu0124-creator](https://clawhub.ai/user/leahlu0124-creator)

### License/Terms of Use:

MIT-0

## Use Case:

External users or employees can use this skill to collect travel invoice PDFs from email, extract invoice and itinerary data, merge supporting PDFs, and produce reimbursement-ready Excel and PDF outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires mailbox access and may handle mailbox passwords or app tokens.

Mitigation: Use a revocable app password or OAuth-style credential where possible, and do not print or paste mailbox credentials into agent-visible output.

Risk: Invoice email attachments can be untrusted files.

Mitigation: Run the workflow in a contained workspace and process only trusted invoice emails and PDF attachments.

Risk: Temporary files and extracted ZIP contents may expose sensitive invoice data or unsafe paths.

Mitigation: Prefer private temporary directories, clean invoice intermediates after use, and use safe ZIP extraction behavior.

Risk: Generated spreadsheets may contain data derived from untrusted attachments.

Mitigation: Open generated workbooks with external links and macros disabled and review reimbursement data before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leahlu0124-creator/skills/invoice-from-email)
- [Tesseract Simplified Chinese language data](https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata)
- [Tesseract for Windows installer wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, Files]

**Output Format:** [Markdown instructions with shell commands; generated intermediates include Markdown and JSON, and final artifacts include merged PDFs and an Excel workbook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes mailbox attachments and local invoice PDFs; output quality depends on PDF format and available OCR dependencies.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
