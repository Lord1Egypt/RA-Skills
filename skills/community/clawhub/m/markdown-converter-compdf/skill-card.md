## Description: <br>
Process, convert, edit, and extract data from PDF files using the ComPDF Cloud API, including format conversion, page manipulation, watermarking, OCR, and structured document extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compdf-youna](https://clawhub.ai/user/compdf-youna) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use this skill to send PDFs, images, and office documents to ComPDF Cloud for conversion, OCR, compression, page editing, watermarking, comparison, and structured extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files and optional document passwords may be sent to ComPDF Cloud for processing. <br>
Mitigation: The skill requires explicit user confirmation before upload and advises users to avoid highly sensitive or confidential documents unless they accept the provider's privacy and retention terms. <br>
Risk: A ComPDF API key may be stored locally if the user chooses to save it. <br>
Mitigation: The skill only stores the key after opt-in, uses it from the local configuration for future sessions, and tells users they can delete the key file to revoke local storage. <br>
Risk: Processing may fail because of unsupported formats, encrypted PDFs, quota limits, or cloud task errors. <br>
Mitigation: The skill checks response body status, looks up failure codes in its error reference, and tells users when to provide a password, retry, split tasks, or address quota exhaustion. <br>


## Reference(s): <br>
- [ComPDF API Reference](https://www.compdf.com/guides/api-reference/v2/overview?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_md_convert&ref_platform_id=clawhub_skills) <br>
- [ComPDF Tool List](references/tool-list.md) <br>
- [ComPDF Parameter Details](references/parameters.md) <br>
- [ComPDF Error Code Reference](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown status messages with file metadata, download links, error codes, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include expiring ComPDF download URLs and task status details returned by the cloud API.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
