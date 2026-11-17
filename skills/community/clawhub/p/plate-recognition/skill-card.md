## Description:

识别车牌号、车牌颜色、单/双层车牌、位置框。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit a license-plate image URL or base64 image data and receive plate number, color, layer type, and bounding-box recognition results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are persisted in a local plaintext .env file.

Mitigation: Use a narrowly scoped Xiaobenyang API key, avoid shared or committed workspaces, and rotate the key if the workspace may have been exposed.

Risk: License-plate images or image URLs are sent to an external Xiaobenyang API.

Mitigation: Use the skill only when users are comfortable sending vehicle image data to that external service and have appropriate privacy clearance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/plate-recognition)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Markdown prose summarizing raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends image URLs or base64 image data to an external Xiaobenyang API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
