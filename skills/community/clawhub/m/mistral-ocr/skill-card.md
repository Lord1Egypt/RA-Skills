## Description:

Extract text, tables, and images from PDFs or images using the Mistral OCR API and output results in Markdown, JSON, or HTML formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzdame](https://clawhub.ai/user/yzdame)

### License/Terms of Use:

MIT

## Use Case:

Developers and document-processing users use this skill to run cloud OCR on PDFs and images, preserving extracted text, tables, and images in Markdown, JSON, or HTML outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are uploaded to Mistral cloud services for OCR processing, which can expose confidential file contents if used with sensitive material.

Mitigation: Process sensitive documents only after confirming Mistral upload is acceptable for the use case; otherwise use an offline OCR tool.

Risk: The Mistral SDK dependency is open-ended, creating a supply-chain review risk.

Mitigation: Pin mistralai to a reviewed non-affected version before installation or deployment.

Risk: Generated HTML may carry content derived from untrusted source documents.

Mitigation: Avoid opening generated HTML from untrusted documents unless it has been reviewed or sanitized.

Risk: The skill requires an API key for Mistral services.

Mitigation: Store the API key in a secret manager or a temporary environment variable rather than committing it to files.

## Reference(s):

- [Mistral API Console](https://console.mistral.ai/home)
- [Mistral Privacy Policy](https://mistral.ai/privacy-policy)
- [ClawHub Skill Page](https://clawhub.ai/yzdame/skills/mistral-ocr)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown, JSON, or HTML files with optional extracted image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Mistral API key in MISTRAL_API_KEY and writes results to a local output directory.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
