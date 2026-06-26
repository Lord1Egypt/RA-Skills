## Description: <br>
Extract tables and text from a PDF into CSV format via the PDFAPIHub cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to convert PDF tables, invoices, reports, and similar documents into CSV for data ingestion, spreadsheet work, CRM import, or ETL workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF files, PDF URLs, and extracted content are sent to pdfapihub.com for processing. <br>
Mitigation: Use the skill only for documents appropriate for that external service, and review the provider's privacy, retention, deletion, and access-control practices before sending confidential or regulated PDFs. <br>
Risk: The skill requires a sensitive PDFAPIHub API key. <br>
Mitigation: Store the API key in the PDFAPIHUB_API_KEY environment variable or an approved secret manager, avoid committing it to source files, and send it only in the CLIENT-API-KEY header. <br>


## Reference(s): <br>
- [PDFAPIHub documentation](https://pdfapihub.com/docs) <br>
- [PDFAPIHub API endpoint](https://pdfapihub.com/api/v1/convert/pdf/csv) <br>
- [ClawHub skill page](https://clawhub.ai/rishabhdugar/pdf-to-csv) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/rishabhdugar) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Configuration instructions] <br>
**Output Format:** [CSV returned as a file, URL, base64 payload, or combined response depending on request parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PDFAPIHub API key in the CLIENT-API-KEY header and accepts a public PDF URL, base64-encoded PDF, or multipart file upload.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
