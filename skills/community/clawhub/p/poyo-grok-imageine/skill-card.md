## Description:

Helps agents prepare and submit PoYo Grok Imagine video-generation jobs for text-to-video and image-to-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to construct PoYo Grok Imagine requests, submit them with a POYO_API_KEY, and track the returned task_id for status polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, callback URLs, and job metadata are sent to the PoYo third-party API.

Mitigation: Confirm the user is comfortable sharing that data with PoYo and avoid submitting secrets or private media.

Risk: API credentials can be exposed if passed directly on a command line or stored in logs.

Mitigation: Use the POYO_API_KEY environment variable, avoid echoing credentials, and rotate keys that may have appeared in shell history or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-grok-imageine)
- [PoYo Grok Imagine model page](https://poyo.ai/models/grok-imagine)
- [PoYo Grok Imagine API docs](https://docs.poyo.ai/api-manual/video-series/grok-imagine)
- [PoYo Grok Imagine OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/grok-imagine.json)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [Artifact API reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the chosen model id, request payload or parameter summary, image-reference usage, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
