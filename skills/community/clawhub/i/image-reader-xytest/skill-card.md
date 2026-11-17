## Description:

Recognizes text in local images, including Chinese text, by sending resized images to the OCR.space API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xytest](https://clawhub.ai/user/xytest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract OCR text from local image files, especially Chinese-language images, through a CLI helper that calls OCR.space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to OCR.space for third-party OCR processing.

Mitigation: Avoid IDs, credentials, medical, financial, legal, or confidential business images unless third-party processing is approved.

Risk: Extracted text is saved locally in a predictable file under the skill scripts directory.

Mitigation: Review and delete generated OCR text files when they may contain sensitive content.

## Reference(s):

- [OCR.space API endpoint](https://api.ocr.space/parse/image)
- [ClawHub skill page](https://clawhub.ai/xytest/skills/image-reader-xytest)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands; OCR helper output is UTF-8 text saved to a local .txt file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local image path as input and returns or stores recognized text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
