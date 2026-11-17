## Description:

Extract tables and text from a PDF into an Excel workbook (XLSX), with each page as a separate sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert PDF invoices, financial statements, reports, purchase orders, and tax documents into Excel workbooks for analysis or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF files, base64 PDF contents, or PDF URLs are sent to pdfapihub.com for conversion.

Mitigation: Use the skill only when third-party processing by pdfapihub.com is permitted; avoid confidential, regulated, financial, tax, or personal documents unless approved by the organization.

## Reference(s):

- [PDF API Hub Documentation](https://pdfapihub.com/docs)
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/pdf-to-xlsx)

## Skill Output:

**Output Type(s):** [API Calls, Files, Configuration instructions, Guidance]

**Output Format:** [Excel workbook (XLSX) returned as URL, base64, both, or file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each PDF page becomes a separate sheet; supports optional page selection and custom output filename.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
