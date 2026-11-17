## Description:

Animate static images into dynamic AI-generated videos using Media.io OpenAPI and a Media.io API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Media.io OpenAPI for image-to-video generation, task result retrieval, and account credit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, task IDs, and credit checks are sent to Media.io.

Mitigation: Use the skill only for content appropriate to send to Media.io and review the service terms before submitting sensitive material.

Risk: Generation calls may consume Media.io account credits.

Mitigation: Check credits before generation and use an account or key with appropriate spending controls.

Risk: A leaked Media.io API key could allow unauthorized API usage.

Mitigation: Store API_KEY in a secret manager or environment variable and avoid exposing it in prompts, logs, or shared files.

## Reference(s):

- [Media.io OpenAPI Documentation](https://platform.media.io/docs/)
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/mediaio-image-to-video-api)
- [Publisher Profile](https://clawhub.ai/user/wondershare-boop)

## Skill Output:

**Output Type(s):** [API calls, JSON, Configuration, Guidance]

**Output Format:** [JSON responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key and sends generation requests to Media.io.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
