## Description:

Extract and return text content from images, screenshots, or scanned documents using DeepSeek OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendream2002](https://clawhub.ai/user/sendream2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract recognized text from local image files, screenshots, and scanned documents by calling a configured DeepSeek OCR service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included CLI can send local image paths to a configurable plaintext OCR service.

Mitigation: Use only a local or trusted OCR endpoint, keep the host on loopback or another trusted network, and avoid sensitive filenames or directories unless the service data handling is documented and acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sendream2002/skills/gt-simon-deepseek-ocr)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object with extracted text and optional OCR metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output may include confidence and model fields when provided by the OCR service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
