## Description:

Combine one or more images into a single PDF document with page layout control (page size, orientation, fit mode, margin).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to combine image URLs, base64 images, or uploaded image files into PDF documents with layout controls for page size, orientation, fit mode, and margins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive, regulated, or confidential images may be sent to pdfapihub.com for conversion.

Mitigation: Use the skill only for content the user is authorized to share with that provider, and review the provider's privacy, retention, and access-control terms before use.

Risk: Default hosted PDF URL output may expose generated documents through a third-party CDN workflow.

Mitigation: Use base64 or file output when hosted links are not acceptable, and avoid converting IDs, medical records, insurance photos, or business documents unless the data-handling terms are approved.

## Reference(s):

- [PDF API Hub](https://pdfapihub.com)
- [PDF API Hub Documentation](https://pdfapihub.com/docs)
- [Image to PDF API Endpoint](https://pdfapihub.com/api/v1/convert/image/pdf)

## Skill Output:

**Output Type(s):** [API Calls, Files, Shell commands, Configuration instructions]

**Output Format:** [JSON responses and PDF file outputs; Markdown with inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return hosted URL, base64, both, or file output; accepts up to 100 images per request.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
