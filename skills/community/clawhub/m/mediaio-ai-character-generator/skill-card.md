## Description:

Generate AI images of girls, characters, and fictional personas using Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate stylized character portraits from an authorized image URL and prompt through Media.io OpenAPI, including submitting a task, polling for completion, and returning generated image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and image URLs are sent to Media.io as the core generation workflow.

Mitigation: Use only non-sensitive image URLs that the user owns or is authorized to process, and make clear that generation uses Media.io.

Risk: The MEDIAIO_API_KEY could be exposed in logs, prompts, or shared transcripts.

Mitigation: Keep the key in an environment variable and redact it from logs, command output, prompts, and responses.

Risk: Generated character images could be mistaken for real identity evidence or unedited media.

Mitigation: Present generated outputs as synthetic or edited content and avoid identity verification or biometric certainty claims.

Risk: The Media.io API may fail due to authentication, validation, insufficient credits, failed tasks, or timeouts.

Mitigation: Check credits before generation, validate image URL and prompt inputs, poll task status, and stop with a clear message on failed, timeout, or insufficient-credit responses.

## Reference(s):

- [Media.io API documentation](https://platform.media.io/docs/)
- [Media.io developer portal](https://developer.media.io/)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-ai-character-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with cURL examples and generated image URLs from API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and user-authorized image URLs; generated image URLs are returned after asynchronous polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
