## Description:

识别植物名称（或所属科, 属, 种或亚种）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to identify plants from an image URL or base64-encoded image data and present the API response in a readable form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant image URLs or base64 image data are sent to an external Xiaobenyang service.

Mitigation: Use only images approved for submission to that service and avoid sending sensitive, private, or regulated image content.

Risk: The Xiaobenyang API key is saved in a local plaintext .env file.

Mitigation: Use a dedicated, revocable key, keep .env protected and out of source control, and rotate the key if it may have been exposed.

Risk: The package contains leftover gaokao or college-admissions references unrelated to plant recognition.

Mitigation: Review those remnants with the publisher before relying on the package in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/plant-recognition)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [Xiaobenyang API key site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key and either an image URL or base64-encoded image data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
