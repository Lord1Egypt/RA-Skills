## Description:

Transforms photos and image URLs into Studio Ghibli-style artwork through the Media.io OpenAPI effects-ghibli workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit authorized image URLs to Media.io, poll asynchronous generation tasks, and return generated preview URLs for edited synthetic artwork.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, sensitive, or internal image URLs could be sent to the external Media.io service.

Mitigation: Use only images and image URLs the user is authorized and comfortable sending to Media.io.

Risk: The Media.io API key could be exposed in logs, chats, or command output.

Mitigation: Keep MEDIAIO_API_KEY in the environment and omit raw API keys from logs and responses.

Risk: Asynchronous polling could run longer than intended.

Mitigation: Stop polling after a reasonable timeout or retry limit and report the last task status.

## Reference(s):

- [Media.io platform documentation](https://platform.media.io/docs/)
- [Media.io developer portal](https://developer.media.io/)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-ghibli-image-filter)
- [Publisher profile](https://clawhub.ai/user/wondershare-boop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples plus bash cURL commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Media.io task IDs and generated preview URLs after polling when invoked.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
