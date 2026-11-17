## Description:

Extract plain text from all or selected pages of a PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract readable text from PDFs for search indexing, AI/LLM processing, content migration, plagiarism checks, and accessibility workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs, PDF URLs, and converted text are sent to pdfapihub.com and CDN infrastructure.

Mitigation: Do not use confidential, regulated, or customer-sensitive PDFs unless the provider's data retention, access control, and compliance terms have been reviewed.

## Reference(s):

- [PDF API Hub documentation](https://pdfapihub.com/docs)
- [PDF API Hub](https://pdfapihub.com)

## Skill Output:

**Output Type(s):** [Text, Files, API Calls, Configuration]

**Output Format:** [Plain text returned by URL, base64, file, or combined output mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PDF URL, base64-encoded PDF, or multipart file upload and a CLIENT-API-KEY header. Optional page selection and output filename are supported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
