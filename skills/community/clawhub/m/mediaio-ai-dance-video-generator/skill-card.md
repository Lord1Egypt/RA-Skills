## Description:

Generate AI dance videos where characters move to music or choreography templates using Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Media.io dance-video generation tasks from authorized image and driving-video URLs, poll for completion, and return generated video preview URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided image and driving-video URLs are sent to Media.io for processing.

Mitigation: Use only media the user owns or is authorized to process, and confirm the user is comfortable sending those URLs to Media.io.

Risk: The skill uses MEDIAIO_API_KEY for credit checks and generation requests.

Mitigation: Keep the API key out of logs and responses, check credits before generation, and stop clearly when credits are insufficient.

## Reference(s):

- [Media.io API Documentation](https://platform.media.io/docs/)
- [Media.io Developer Platform](https://developer.media.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and cURL commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and user-provided image and video URLs; generated media URLs are returned after asynchronous polling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
