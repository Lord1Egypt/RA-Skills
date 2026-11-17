## Description:

Generate AI images from text descriptions using Media.io OpenAPI, including Imagen 4 and Soul Character models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure Media.io text-to-image generation, submit prompts, and poll task results for generated image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Media.io API key and sends requests to Media.io.

Mitigation: Run it in a dedicated environment, use a scoped or replaceable API key where possible, and avoid sharing the key outside the runtime environment.

Risk: The bundled router can query the account credits balance even though the main description focuses on text-to-image generation.

Mitigation: Review whether the Credits API is needed before deployment and restrict or remove that invocation path when credit lookup is outside the intended use.

Risk: Image generation and credit checks may consume or expose account-level Media.io usage information.

Mitigation: Use an approved Media.io account, monitor credit usage, and confirm that prompts and generated content are appropriate for the account's policy obligations.

## Reference(s):

- [Media.io API documentation](https://platform.media.io/docs/)
- [Media.io developer homepage](https://developer.media.io/)
- [Media.io pricing and credits](https://developer.media.io/pricing.html)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-text-to-image-api)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; API invocations return JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key and returns asynchronous task identifiers that must be checked through the task result API.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
