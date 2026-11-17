## Description:

Generate images from text descriptions using AI models through OATDA's unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent to generate AI images, artwork, illustrations, mockups, and concept art through OATDA-supported image models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented shell command pattern can allow prompt text to be interpreted by the local shell if user input is interpolated unsafely.

Mitigation: Build request JSON with a safe encoder such as jq --arg before execution, and review generated shell commands before running them.

Risk: Image prompts are sent to an external OATDA API using locally supplied credentials.

Mitigation: Avoid confidential or regulated prompt content and prefer a controlled OATDA_API_KEY environment variable over automatic credential-file fallback.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/devcsde/skills/oatda-generate-image)
- [OATDA](https://oatda.com)
- [OATDA image model discovery endpoint](https://oatda.com/api/v1/llm/models?type=image)
- [OATDA image generation endpoint](https://oatda.com/api/v1/llm/generate-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces image URLs and may surface a revised prompt when the external API returns one.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
