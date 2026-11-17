## Description:

Combine two or more PDFs into a single document. Supports URLs, base64, multipart uploads, and custom metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to combine invoices, reports, contracts, chapters, or other PDF packets into one document through the pdfapihub.com merge API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs, source URLs, optional metadata, and the CLIENT-API-KEY value are sent to pdfapihub.com for processing.

Mitigation: Use only documents approved for third-party processing, and avoid confidential, regulated, or internal-only documents unless that processing has been approved for the use case.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/merge-pdfs)
- [PDF API Hub Documentation](https://pdfapihub.com/docs)
- [PDF API Hub](https://pdfapihub.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Configuration instructions, Shell commands, Guidance]

**Output Format:** [JSON API request and response examples, with optional merged PDF URL, file, or base64 output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header; accepts 2-25 PDF inputs as URLs, base64 data, or multipart files, with optional output filename and PDF metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
