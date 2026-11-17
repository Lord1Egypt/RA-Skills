## Description:

Performs cloud-based OCR on PNG, JPG, JPEG, and WEBP images using SiliconFlow's DeepSeek-OCR with automatic image preprocessing for improved recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwq2023qwq](https://clawhub.ai/user/qwq2023qwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to extract text from local image files or image URLs through a cloud OCR API. It is suited for OCR workflows where third-party processing of the submitted image is approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images and the API key are sent to SiliconFlow or the configured API host.

Mitigation: Use the skill only for images approved for third-party cloud processing, keep the API key protected, and verify config.json before each use.

Risk: The configurable API host can receive sensitive image content if changed to an untrusted endpoint.

Mitigation: Review the baseUrl setting before deployment and prefer a version that validates the API host.

Risk: Unpinned Python dependencies may resolve to different package versions over time.

Mitigation: Pin and review dependency versions before use in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qwq2023qwq/skills/online-deepseek-ocr)
- [Publisher profile](https://clawhub.ai/user/qwq2023qwq)
- [SiliconFlow](https://siliconflow.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text or JSON OCR results, with setup guidance that may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and an API key; local images may be preprocessed and uploaded as base64 to the configured API host.]

## Skill Version(s):

1.0.2 (source: server release metadata, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
