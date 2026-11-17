## Description:

Generate high-quality, photorealistic images from text prompts using Google Imagen 4 via Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call Media.io OpenAPI for Imagen 4 text-to-image generation and to retrieve generation task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Media.io API key and sends prompts to Media.io OpenAPI.

Mitigation: Use a dedicated, limited-privilege API key if available, avoid sensitive prompt content, and review generated outputs before use.

Risk: The artifact includes a credit-balance API in addition to the advertised image-generation workflow.

Mitigation: Review the credits endpoint before installation or execution and restrict use to the APIs expected for the deployment.

Risk: The quick-start dependency example installs requests without a pinned version.

Mitigation: Install dependencies from a pinned, reviewed environment for production or shared deployments.

## Reference(s):

- [Media.io API documentation](https://platform.media.io/docs/)
- [Media.io developer portal](https://developer.media.io/)
- [ClawHub skill listing](https://clawhub.ai/wondershare-boop/skills/mediaio-imagen4-image-generator)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Python and shell examples; API responses are JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key supplied through API_KEY or passed explicitly.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
