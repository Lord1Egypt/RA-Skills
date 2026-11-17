## Description:

GLM-OCR-SDK helps agents parse document images, PDFs, scans, and screenshots with the GLM-OCR SDK, returning Markdown plus structured JSON regions with labels and bounding boxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when an agent needs to extract text, tables, formulas, or structured content from visual documents. It is intended for document OCR workflows, not real-time camera feeds, audio transcription, or non-document images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if passed on the command line or stored in a repository .env file.

Mitigation: Use protected environment variables or a secret manager, and avoid committing .env files.

Risk: Cloud OCR mode sends submitted documents to Zhipu, which may be inappropriate for confidential material.

Mitigation: Use self-hosted mode or avoid processing sensitive documents unless cloud processing is approved.

Risk: OCR output can be incomplete or malformed, including model-returned JSON that remains a raw string.

Mitigation: Check results for an error key and validate extracted JSON or Markdown before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaredforreal/skills/glmocr-sdk)
- [GLM-OCR SDK homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and CLI/Python usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY for cloud MaaS mode; saved results may include JSON, Markdown, cropped images, and optional layout visualizations.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
