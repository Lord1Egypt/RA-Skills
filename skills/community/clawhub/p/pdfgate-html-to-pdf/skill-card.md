## Description:

HTML to PDF conversion with the PDFGate PDF API. Generate PDF invoices, reports, receipts and fillable PDF forms from HTML or a web page URL using a dependency-free Node.js script with page size, margin and orientation options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdfgate](https://clawhub.ai/user/pdfgate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can convert HTML documents or public web pages into PDFs for invoices, reports, receipts, letters, certificates, and fillable forms, with control over page layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML documents, webpage content, and header or footer templates are sent to PDFGate for rendering.

Mitigation: Get approval before submitting sensitive, confidential, or third-party content.

Risk: The skill requires a PDFGate API key, and production requests may incur account charges.

Mitigation: Protect the API key, use a sandbox key for trials, and account for production usage charges.

## Reference(s):

- [PDFGate HTML to PDF API](https://pdfgate.com/api/html-to-pdf)
- [Generate PDF endpoint reference](https://pdfgate.com/documentation/generate-pdf)
- [Fillable fields from HTML guide](https://pdfgate.com/guides/html-to-pdf/add-fillable-fields)
- [PDFGate authentication documentation](https://pdfgate.com/documentation/authentication)

## Skill Output:

**Output Type(s):** [Files]

**Output Format:** [PDF document, optionally with fillable form fields]

**Output Parameters:** [HTML or public webpage URL; page size, orientation, margins, scale, media type, page ranges, wait options, and fillable fields]

**Other Properties Related to Output:** [Saved to the user-selected local .pdf path.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
