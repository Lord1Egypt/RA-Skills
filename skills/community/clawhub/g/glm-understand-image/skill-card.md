## Description:

Uses the GLM Vision MCP server to help an agent understand and analyze images, screenshots, technical diagrams, data visualizations, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thincher](https://clawhub.ai/user/thincher)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to configure a GLM Vision MCP server and ask an agent to analyze local or URL-based images, extract screenshot text, diagnose error screenshots, interpret diagrams, compare UI screenshots, and summarize video content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable npm-hosted MCP tooling locally.

Mitigation: Install only in environments where unpinned third-party npm packages are acceptable, and prefer a version-pinned revision before broad deployment.

Risk: Image or video content may be sent to the GLM/Zhipu service.

Mitigation: Avoid sending sensitive screenshots, images, or videos unless they are redacted and approved for external processing.

Risk: API key handling may expose credentials through local files, logs, or transcripts.

Mitigation: Use a low-privilege API key, restrict permissions on ~/.openclaw/config/glm.json, and rotate the key if exposure is suspected.

## Reference(s):

- [GLM Vision MCP Server documentation](https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server)
- [ClawHub skill page](https://clawhub.ai/thincher/skills/glm-understand-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Zhipu/GLM API key and can process image paths, image URLs, screenshots, diagrams, visualizations, UI comparisons, and supported video files.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
