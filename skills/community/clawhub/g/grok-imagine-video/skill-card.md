## Description:

xAI Grok Imagine API integration for image generation, text-to-video, image-to-video, and editing via natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devvgwardo](https://clawhub.ai/user/devvgwardo)

### License/Terms of Use:

MIT

## Use Case:

Developers and bot operators use this skill to generate and edit images and videos through xAI's Grok Imagine APIs, including chat workflows with async polling, progress updates, and media delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, and generated media requests are sent to xAI.

Mitigation: Avoid sensitive or regulated content and review prompts and media before sending them to the API.

Risk: The helper client accepts a configurable API base URL, which could expose the xAI API key to an unintended endpoint.

Mitigation: Use the default xAI endpoint, do not pass custom API base URLs, and keep the xAI key scoped and monitored.

Risk: Bot integrations that accept untrusted download URLs or output paths could fetch remote files or write media to unintended locations.

Mitigation: Restrict who can provide URLs and output paths, validate media sources, and constrain downloads to controlled workspace locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devvgwardo/skills/grok-imagine-video)
- [xAI Model Capabilities](https://docs.x.ai/developers/model-capabilities)
- [xAI Image Generation API](https://docs.x.ai/developers/model-capabilities/images/generation)
- [xAI Video Generation API](https://docs.x.ai/developers/model-capabilities/video/generation)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [xAI Grok Imagine API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Files]

**Output Format:** [Python client calls with JSON API responses and downloaded image or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY; generated media URLs are temporary, and video jobs are polled asynchronously.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
