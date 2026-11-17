## Description:

Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to OCR local image files into text or structured JSON without sending document contents to an external OCR API. It is suited for extracting Chinese and English text from screenshots, documents, and other user-provided local images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and first-run language data downloads may introduce supply-chain exposure.

Mitigation: Review or pin the tesseract.js dependency and run the skill only after accepting npm package and language-data downloads.

Risk: OCR output may contain credentials, secrets, or sensitive document text.

Mitigation: Review and redact extracted text before display, storage, or sharing; do not route OCR output to network-capable commands or external endpoints.

Risk: Fetching remote images for OCR can process content the user did not intentionally provide.

Mitigation: Process only local filesystem images that the user explicitly selected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/ocr-local-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)
- [Tesseract.js project](https://github.com/naptha/tesseract.js)
- [Faberlens safety evaluation](https://faberlens.ai/explore/ocr-local)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON OCR output, usually accompanied by concise Markdown guidance and local shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output includes recognized text, confidence, and word-level bounding boxes when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
