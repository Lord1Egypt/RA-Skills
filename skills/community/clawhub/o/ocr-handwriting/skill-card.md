## Description:

输入包含手写文本的图像，自动检测文本行并识别内容。适用于手写笔记、签名、手写表单等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit handwriting images by URL or base64 data and receive OCR results for notes, signatures, and handwritten forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XBY API key in plaintext in a .env file.

Mitigation: Use a limited or revocable API key, restrict filesystem access where practical, and remove the .env key after use.

Risk: Handwritten images are sent to a remote Xiaobenyang service for OCR processing.

Mitigation: Avoid submitting sensitive forms, signatures, or personal data unless remote processing by this service is acceptable.

Risk: The security review marked the release suspicious because of plaintext key storage and copied or mismatched gaokao instructions.

Mitigation: Review the skill instructions and scanner summary before deployment, and confirm the actual OCR behavior in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr-handwriting)
- [Xiaobenyang service site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured API result data with success, raw, and message fields, usually summarized for the user as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key and either an image URL or base64-encoded image data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
