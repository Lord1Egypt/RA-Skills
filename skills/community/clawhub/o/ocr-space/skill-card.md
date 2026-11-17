## Description:

Calls the OCR.space free API to extract text from image files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juguangyuan520-dotcom](https://clawhub.ai/user/juguangyuan520-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send image files to OCR.space for multilingual OCR and receive recognized text from command-line or Python workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to OCR.space for processing.

Mitigation: Use only with images that are acceptable to share with the external OCR.space service; avoid sensitive or regulated documents unless that sharing is approved.

Risk: The compression behavior can overwrite or delete a predictable local *_compressed.jpg file.

Mitigation: Run with ordinary user privileges in directories without valuable matching compressed-image files, and replace the predictable path with a secure temporary file before broader deployment.

## Reference(s):

- [OCR.space OCR API documentation](https://ocr.space/ocrapi)
- [ClawHub skill page](https://clawhub.ai/juguangyuan520-dotcom/skills/ocr-space)
- [ClawHub publisher profile](https://clawhub.ai/user/juguangyuan520-dotcom)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text and Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload image data to OCR.space and may create a temporary compressed JPEG for files over the free API size limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
