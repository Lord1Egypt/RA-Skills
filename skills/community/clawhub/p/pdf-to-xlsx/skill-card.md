## Description: <br>
Extract tables and text from a PDF into an Excel workbook (XLSX). Each page becomes a separate sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to convert PDF invoices, financial statements, reports, purchase orders, and tax documents into Excel workbooks for review and downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded PDFs or PDF URLs are sent to pdfapihub.com for processing. <br>
Mitigation: Avoid confidential, regulated, financial, legal, or tax documents unless that provider's privacy, retention, and security terms are acceptable for the intended use. <br>
Risk: The skill requires a sensitive API key in the CLIENT-API-KEY header. <br>
Mitigation: Store the API key in a secret manager or protected environment variable, avoid committing it to skill files or logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [PDF API Hub](https://pdfapihub.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Shell commands, Configuration instructions] <br>
**Output Format:** [XLSX file URL or base64/file response, with JSON request examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PDF API Hub API key in the CLIENT-API-KEY header and accepts a public PDF URL, base64 PDF, or multipart file upload.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
