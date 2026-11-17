## Description:

Generate AI images using ByteDance Seedream via Media.io OpenAPI. Delivers high aesthetic quality and detailed rendering for text-to-image and image-to-image tasks with 4K support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route text-to-image and image-to-image generation requests to ByteDance Seedream 4.0 through the Media.io OpenAPI, then query task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and the Media.io API key are sent to Media.io when the skill is used.

Mitigation: Use the skill only where that data sharing is acceptable, keep the API key out of logs and shared prompts, and prefer an isolated environment.

Risk: Generation requests can spend Media.io account credits.

Mitigation: Monitor account credit usage and confirm expected cost exposure before repeated or automated use.

Risk: Unpinned dependencies can change behavior if this skill is packaged for repeated use.

Mitigation: Pin runtime dependencies, including the HTTP client library, in any managed deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-seedream-image-generator)
- [Media.io API documentation](https://platform.media.io/docs/)
- [Media.io developer portal](https://developer.media.io/)
- [Seedream 4.0 generation endpoint](https://openapi.media.io/generation/seedream/i2i-seedream-v4-0)
- [Media.io credit pricing](https://developer.media.io/pricing.html)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key and returns task identifiers or generation-result payloads from Media.io.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
