## Description:

Calls Media.io OpenAPI to create an asynchronous image gender-swap task and return generated image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit authorized portrait image URLs to Media.io for task-based gender-swap image generation and to poll for the resulting edited image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The top-level description may mislead users into expecting Studio Ghibli-style generation rather than Media.io gender-swap behavior.

Mitigation: Review the skill before installing and use it only when the intended task is Media.io gender-swap image editing.

Risk: Images are sent to Media.io using the user's API key.

Mitigation: Submit only images the user is authorized to edit and comfortable sending to Media.io, and keep MEDIAIO_API_KEY out of logs and responses.

Risk: The API is asynchronous and may return pending, failed, timeout, authentication, validation, or insufficient-credit statuses.

Mitigation: Check credits before generation, poll by task_id until a terminal status, stop on insufficient credits, and include trace_id when troubleshooting failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-ai-gender-swap)
- [Media.io platform](https://developer.media.io/)
- [Media.io API documentation](https://platform.media.io/docs/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and image URLs reachable by Media.io servers.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
