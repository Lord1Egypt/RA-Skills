## Description:

识别身份证正面（姓名、性别、民族、出生日期、住址、身份证号）和背面（签发机关、有效期限），自动判断正反面并校验身份证号有效性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract structured fields from Chinese ID-card front or back images supplied as an image URL or Base64 image data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full ID-card image links or Base64 images may be sent to the Xiaobenyang service.

Mitigation: Use only with consent and with required retention, deletion, and regulated-data handling controls in place outside the skill.

Risk: The Xiaobenyang API key is stored in a local plaintext .env file.

Mitigation: Restrict local file access, avoid shared workspaces for credential storage, and rotate the API key if exposure is suspected.

Risk: OCR output can contain sensitive identity fields such as name, address, ID number, issuing authority, and validity period.

Mitigation: Limit display, logging, and onward sharing of OCR results to the minimum necessary for the user's approved workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/ocr-id-card)
- [ALinkLab publisher profile](https://clawhub.ai/user/alinklab)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang MCP endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls]

**Output Format:** [Markdown summary of JSON OCR results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key and an ID-card image URL or Base64 image input.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
