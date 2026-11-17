## Description:

AI Age Filter helps agents apply older or younger face transformation effects to user-authorized image URLs through Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to call Media.io OpenAPI to generate older or younger edited versions of user-authorized face images. It is suited to asynchronous task creation and polling workflows that return generated preview URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided image URLs to Media.io using a Media.io API key.

Mitigation: Use only user-authorized images and avoid processing images the user lacks rights to submit.

Risk: Generated preview URLs represent synthetic edited media.

Mitigation: Present generated outputs as edited synthetic content and avoid claims of identity verification or biometric certainty.

Risk: API keys could be exposed through logs or responses.

Mitigation: Keep MEDIAIO_API_KEY in the environment and avoid printing raw credentials in logs or user-facing output.

## Reference(s):

- [Media.io API Documentation](https://platform.media.io/docs/)
- [Media.io Developer Platform](https://developer.media.io/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY, a user-authorized image URL, and polling by task_id before returning generated preview URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
