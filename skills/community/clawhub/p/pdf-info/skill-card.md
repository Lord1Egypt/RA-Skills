## Description:

Get PDF metadata, encryption status, page count, and file size. Useful for pre-flight checks before processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to inspect PDFs before processing, including checking encryption status, page count, file size, and document metadata for validation, routing, display, and quota decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF URLs, uploaded PDFs, or base64 PDF content are sent to pdfapihub for processing.

Mitigation: Avoid confidential documents unless the provider's terms, retention practices, and access controls meet the user's requirements.

## Reference(s):

- [PDF API Hub Documentation](https://pdfapihub.com/docs)

## Skill Output:

**Output Type(s):** [json, guidance]

**Output Format:** [JSON response with PDF encryption status, page count, file size, and document metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PDF URL, base64 PDF content, or multipart file upload; requires CLIENT-API-KEY authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
