## Description:

Extract text from images using Tesseract.js OCR, with support for Simplified Chinese, Traditional Chinese, and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaw555](https://clawhub.ai/user/shaw555)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to extract machine-readable text from local image files, including screenshots and document photos. It is intended for Chinese and English OCR workflows that need plain text or structured JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill fetches the npm dependency tesseract.js, and first OCR runs may download language data of about 20MB per language.

Mitigation: Pin dependencies, add a lockfile, review the installed tesseract.js version, and allow runtime downloads only in approved environments.

Risk: OCR accuracy can vary for handwritten text, low-contrast images, poorly lit photos, or incorrect language selection.

Mitigation: Review extracted text before relying on it, use clear high-contrast images, and choose the most specific supported language code.

## Reference(s):

- [OCR Test ClawHub release page](https://clawhub.ai/shaw555/skills/ocr-skill-test)
- [Tesseract.js project](https://github.com/naptha/tesseract.js)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Plain text, or JSON containing recognized text, confidence scores, words, and bounding boxes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress messages are written to stderr; OCR quality depends on image clarity and selected language data.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
