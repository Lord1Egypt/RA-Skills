## Description:

兼顾速度与精度的文字识别。输入包含文本的图像，自动检测并识别内容。适用于各类文档、广告牌、屏幕截图等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to send image URLs or base64-encoded images for OCR and receive extracted text for documents, screenshots, signs, and similar image-based text sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images or base64 image data are sent to XiaoBenYang's remote API for OCR processing.

Mitigation: Use the skill only when remote processing is acceptable, and avoid sensitive documents unless the workspace owner has approved that data flow.

Risk: The skill asks for an API key and stores it in a local .env file in plaintext.

Mitigation: Use a trusted workspace, avoid sharing the project directory or .env file, and rotate the API key if the workspace may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr)
- [XiaoBenYang](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text summary of OCR results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tool response includes success status, raw OCR data, and a status message.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
