## Description:

输入常见验证码图片，返回验证码文本内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit common CAPTCHA images by URL or Base64 and receive recognized text from the XiaoBenYang remote OCR service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in plaintext in a local .env file.

Mitigation: Use a disposable or limited API key, keep the workspace private, and remove or rotate the key after use.

Risk: CAPTCHA images, image URLs, and the API key may be sent to the remote XiaoBenYang service.

Mitigation: Submit only CAPTCHA data you are comfortable sharing with that service and review its data handling practices before production use.

Risk: The security review notes that the remote endpoint is configurable.

Mitigation: Confirm the configured endpoint before execution and restrict use to trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr-captcha)
- [XiaoBenYang service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Text summary with raw API JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured XiaoBenYang API key before OCR requests can be made.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
