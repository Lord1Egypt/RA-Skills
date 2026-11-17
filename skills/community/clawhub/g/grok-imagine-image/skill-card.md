## Description:

Generate images with xAI Grok Imagine models, including batch generation, aspect ratios, base64 output, and concurrent requests via the xAI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate AI images, batches of image variations, and URL or base64 image outputs with xAI Grok Imagine models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and generation requests are sent to xAI as part of the skill's stated purpose.

Mitigation: Use this skill only when xAI is the intended provider, and avoid sending sensitive prompts or confidential material.

Risk: The skill requires an XAI_API_KEY credential for API calls.

Mitigation: Provide the API key through the environment and avoid placing credentials directly in prompts, files, or shared command history.

Risk: The trigger wording is broad enough that general image-generation requests may use xAI by default.

Mitigation: Direct the agent to use another provider or disable the skill when xAI should not handle a request.

## Reference(s):

- [xAI Image Generation Documentation](https://docs.x.ai/developers/model-capabilities/images/generation)
- [ClawHub Skill Page](https://clawhub.ai/maliot100x/skills/grok-imagine-image)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration]

**Output Format:** [Markdown with curl, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY and may produce temporary image URLs or base64 image data when the generated API calls are executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
