## Description:

识别营业执照的统一社会信用代码、名称、法定代表人、注册资本、成立日期、经营范围、登记机关和住所地址。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Organizations and developers use this skill to extract structured fields from Chinese business-license images provided as a URL or base64-encoded image data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business-license images and extracted fields are sent to XiaoBenYang's API.

Mitigation: Use the skill only when sending this data to XiaoBenYang is acceptable for the user's business, privacy, and data-handling requirements.

Risk: The API key is persisted in a plaintext .env file.

Mitigation: Use a dedicated, revocable API key, keep .env out of commits and shared archives, and rotate or remove the key when the workspace may be exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr-biz-license)
- [ClawHub publisher profile](https://clawhub.ai/user/xby-skill)
- [XiaoBenYang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, configuration guidance]

**Output Format:** [JSON API response summarized as user-facing text or markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and a business-license image supplied by URL or base64 data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
