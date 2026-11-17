## Description:

Extract tables and text from a PDF into CSV format via the PDFAPIHub cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to convert PDF tables and text into CSV for data pipelines, CRM imports, inventory tracking, spreadsheet workflows, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided PDFs are uploaded to a hosted third-party conversion service.

Mitigation: Only process documents when PDFAPIHub's retention and privacy terms are acceptable, and avoid confidential PDFs unless the service is approved for that data.

Risk: The skill requires a PDFAPIHub API key for conversion requests.

Mitigation: Store the API key in the PDFAPIHUB_API_KEY environment variable or equivalent secret storage, and avoid embedding credentials in prompts, examples, or shared files.

## Reference(s):

- [PDFAPIHub](https://pdfapihub.com)
- [PDFAPIHub Documentation](https://pdfapihub.com/docs)
- [PDF to CSV API Endpoint](https://pdfapihub.com/api/v1/convert/pdf/csv)
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/pdf-to-csv)

## Skill Output:

**Output Type(s):** [Files, API Calls, Configuration instructions]

**Output Format:** [CSV returned as a file, URL, base64 payload, or both]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PDFAPIHub API key and sends user-provided PDFs to PDFAPIHub for processing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
