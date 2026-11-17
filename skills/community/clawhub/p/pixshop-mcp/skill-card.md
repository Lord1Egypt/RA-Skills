## Description:

Pixshop MCP integrates 28+ Pixshop AI creative tools for image generation, photo editing, video creation, virtual try-on, face swap, style transfer, and creative effects in Claude-compatible MCP clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure and operate Pixshop's MCP endpoint from Claude-compatible clients for image generation, image editing, video generation, product media, prompt discovery, and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports broad local Bash and file-read authority that is not needed for the remote Pixshop image and video workflow.

Mitigation: Review requested permissions before installation and prefer a version that removes unnecessary Bash and local file-read permissions.

Risk: Using the workflow may send prompts, image URLs, portraits, product images, and publishable media to Pixshop and backend providers it uses.

Mitigation: Avoid confidential or regulated content unless Pixshop's terms, privacy practices, and provider handling meet the user's requirements.

## Reference(s):

- [Pixshop](https://pixshop.app)
- [Pixshop MCP endpoint](https://pixshop.app/api/mcp)
- [Nano Banana Apps](https://pixshop.app/apps)
- [Pixshop Prompt Library](https://pixshop.app/prompt-library)
- [Pixshop Effects](https://pixshop.app/effects)
- [Pixshop Design Agent](https://pixshop.app/agent)
- [Pixshop Pricing](https://pixshop.app/pricing)
- [ClawHub skill page](https://clawhub.ai/lizhijun/skills/pixshop-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, API Calls]

**Output Format:** [Markdown guidance with JSON MCP configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include prompts, image URLs, video workflow guidance, and Pixshop MCP tool invocations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
