## Description:

Convert photos and images into cartoon-style illustrations using Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit user-authorized image URLs to Media.io, poll asynchronous cartoon-conversion tasks, and return generated preview URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs submitted through the skill are sent to Media.io for processing.

Mitigation: Use only user-provided or user-authorized images, and avoid private images unless their URLs are intentionally reachable by Media.io and permitted by the user's data-handling requirements.

Risk: Media.io API use depends on an API key and may consume credits or billing quota.

Mitigation: Check available credits before generation and keep MEDIAIO_API_KEY out of logs, transcripts, and responses.

## Reference(s):

- [Media.io Developer Platform](https://developer.media.io/)
- [Media.io API Documentation](https://platform.media.io/docs/)
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/mediaio-image-to-cartoon-generator)
- [Publisher Profile](https://clawhub.ai/user/wondershare-boop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task status guidance and generated image preview URLs when Media.io completes the task.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
