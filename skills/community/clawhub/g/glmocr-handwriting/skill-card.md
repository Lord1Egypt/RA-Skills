## Description:

Official skill for recognizing handwritten text from images using ZhiPu GLM-OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to extract handwritten text from images, PDFs, or remote file URLs and convert handwritten or mixed handwritten/printed content into editable text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, PDFs, or remote file URLs are sent to ZhiPu's OCR service for processing.

Mitigation: Use the skill only when external OCR processing is acceptable for the document's privacy, data handling, and compliance requirements.

Risk: The skill requires a ZHIPU_API_KEY for authentication.

Mitigation: Provide the key through the configured environment variable and avoid exposing it in prompts, shared files, logs, or saved OCR output.

## Reference(s):

- [Skill homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr-handwriting)
- [ZhiPu Layout Parsing API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90)
- [ZhiPu API keys](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [JSON result containing extracted Markdown text, layout details, source metadata, and errors; the agent presents the extracted text in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write result JSON to a file and can include the raw upstream API response only when requested with --include-raw.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
