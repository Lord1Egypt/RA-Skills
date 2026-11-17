## Description:

Extract invoice information from images and PDF files using Baidu OCR API, export to Excel, and support single-file, multi-file, directory, and batch processing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitanjp](https://clawhub.ai/user/aitanjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can use this skill to extract structured invoice fields from PDF or image invoices and export them into Excel reports. It is intended for invoice recognition, receipt processing, batch invoice conversion, and reviewable reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Baidu OCR credentials may be stored in config.txt or passed on the command line, and setup.md includes sample-looking key values.

Mitigation: Use environment variables or a secret manager, replace any sample-looking values before use, and exclude local credential files from version control and shared artifacts.

Risk: Invoice images and PDFs are sent to Baidu OCR endpoints for processing.

Mitigation: Confirm the invoices may be shared with Baidu OCR under applicable privacy, customer, and data residency requirements before processing them.

Risk: Generated XLSX reports may contain sensitive invoice data or unsafe spreadsheet content derived from untrusted invoice text.

Mitigation: Treat exported workbooks as sensitive files, restrict sharing, and sanitize or review formula-like values before opening reports in spreadsheet software.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aitanjp/skills/invoice-extractor)
- [Baidu OCR Product](https://cloud.baidu.com/product/ocr)
- [Baidu OCR Documentation](https://cloud.baidu.com/doc/OCR/index.html)
- [Baidu VAT Invoice OCR Endpoint](https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice)
- [Baidu OCR Token Endpoint](https://aip.baidubce.com/oauth/2.0/token)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent workflow may configure Baidu OCR credentials, process local invoice PDFs or images, and generate XLSX reports containing extracted invoice fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
