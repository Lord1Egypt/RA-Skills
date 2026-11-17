## Description:

Convert PDF pages to images (PNG, JPG, or WebP). Supports DPI control, resize, background color, and page selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document workflow teams use this skill to convert selected PDF pages into PNG, JPG, or WebP images for thumbnails, previews, social media images, print exports, and slide extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF files or PDF URLs are sent to pdfapihub.com for processing.

Mitigation: Do not use confidential, regulated, or internal-only documents unless the organization has approved the provider and its retention and privacy practices.

Risk: The skill requires an API key in the CLIENT-API-KEY header.

Mitigation: Store the key in an approved secret manager or environment variable, avoid including it in shared prompts or files, and rotate it if exposed.

Risk: URL output can place generated images behind externally hosted links.

Mitigation: Use base64 or file output when externally hosted image links are not appropriate for the document sensitivity or workflow.

## Reference(s):

- [PDF API Hub documentation](https://pdfapihub.com/docs)
- [PDF to Image API endpoint](https://pdfapihub.com/api/v1/convert/pdf/image)
- [ClawHub skill page](https://clawhub.ai/rishabhdugar/skills/pdf-to-image)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell commands; API responses may contain image URLs, base64 image data, or downloadable image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PNG, JPG, JPEG, and WebP output, page selection, DPI from 72 to 300, resize dimensions up to 10000 px, and up to 100 pages per request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
