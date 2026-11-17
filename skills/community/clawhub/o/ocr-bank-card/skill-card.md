## Description:

识别银行卡号、发卡银行和卡类型，使用 Luhn 算法校验卡号有效性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to recognize a bank card number, issuing bank, and card type from an image URL or base64-encoded image, then check the card number with the Luhn algorithm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank-card images or image URLs are sent to the XiaoBenYang API.

Mitigation: Use the skill only when the user accepts that external processing, and avoid submitting images with security codes or unnecessary personal details.

Risk: The API key may be stored in a local plaintext .env file.

Mitigation: Prefer secret-manager storage where available and rotate the API key if the local file is exposed.

Risk: Recognized card numbers may be displayed without masking.

Mitigation: Mask card numbers in user-facing summaries unless full output is explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr-bank-card)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, raw API response data, and a status message.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
