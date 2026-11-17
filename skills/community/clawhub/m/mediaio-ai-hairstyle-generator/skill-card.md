## Description:

Try different hairstyles and accessories on photos using AI via Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit user-authorized portrait image URLs to Media.io's asynchronous hairstyle generation API, poll task status, and return generated preview URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-authorized portrait image URLs are sent to Media.io for processing.

Mitigation: Avoid private or sensitive images unless Media.io retention and sharing terms are acceptable for the use case.

Risk: The Media.io API key could be exposed in logs or shared transcripts.

Mitigation: Keep MEDIAIO_API_KEY in environment configuration and avoid echoing raw credentials in responses, logs, or command examples.

## Reference(s):

- [Media.io API documentation](https://platform.media.io/docs/)
- [Media.io developer platform](https://developer.media.io/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and a user-authorized image URL; returns task status and generated preview URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
