## Description:

MiniMax Vision uses a configured MiniMax MCP service to analyze user-provided images and return image-understanding results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route image-analysis requests to MiniMax MCP and return concise image recognition results to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and prompts may be processed by the configured MiniMax MCP service without enough user confirmation or disclosure.

Mitigation: Ask for explicit user confirmation before sending image content and disclose the configured service handling the image.

Risk: Sensitive photos, IDs, documents, private screenshots, or confidential business images could be sent to an external image-analysis service.

Mitigation: Avoid sensitive images unless the service configuration, retention policy, and organizational approval are acceptable.

Risk: Unvalidated image paths could allow analysis of files outside the intended inbound media directory.

Mitigation: Validate image paths against the inbound media directory and accepted image extensions before invoking the MCP call.

Risk: The helper script modifies PATH with a hard-coded local directory.

Mitigation: Remove the hard-coded PATH modification and rely on documented runtime configuration for mcporter.

## Reference(s):

- [MiniMax Vision Skill Page](https://clawhub.ai/hongjiahao371-pixel/skills/minimax-vision)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown response with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns MiniMax MCP image-analysis output for a supplied image path and prompt.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
