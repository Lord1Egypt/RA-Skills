## Description: <br>
Get PDF metadata, encryption status, page count, and file size. Useful for pre-flight checks before processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-workflow builders use this skill to inspect PDF metadata, encryption status, page count, and file size before routing or processing PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs, PDF URLs, and extracted metadata are submitted to pdfapihub.com for processing. <br>
Mitigation: Use only documents approved for third-party processing; avoid confidential, regulated, internal, or signed-access document URLs unless third-party processing is approved. <br>
Risk: The skill requires a CLIENT-API-KEY credential. <br>
Mitigation: Protect the API key like any other credential and avoid placing real keys in shared prompts, examples, logs, or committed files. <br>


## Reference(s): <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [PDF API Hub](https://pdfapihub.com) <br>
- [ClawHub PDF Info Skill](https://clawhub.ai/rishabhdugar/pdf-info) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response data and Markdown guidance with optional curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header and one PDF input as a URL, base64 payload, or multipart file upload.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
