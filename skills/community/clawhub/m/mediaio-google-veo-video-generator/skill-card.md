## Description:

Generate cinematic-quality AI videos from text and image inputs using Google Veo 3.1 through the Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external creators use this skill to connect an agent to Media.io for Google Veo image-to-video generation, credit checks, and task-result polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, task IDs, and the API key are sent to Media.io's external API when the skill is invoked.

Mitigation: Use the skill only for intended Media.io workflows, keep API keys out of logs, shell history, and source control, and avoid confidential prompts, private image URLs, or sensitive task IDs unless Media.io processing is acceptable.

Risk: A missing or mishandled API key can prevent use or expose account credentials.

Mitigation: Provide the key through API_KEY or an explicit runtime parameter, and rotate the key if it is shared or exposed.

## Reference(s):

- [Media.io OpenAPI documentation](https://platform.media.io/docs/)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-google-veo-video-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell examples; API responses are JSON objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API_KEY. Generation calls return a task_id that should be polled with Task Result.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
