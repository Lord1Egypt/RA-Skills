## Description:

Use PoYo AI Grok Imagine Video for short text-to-video and image-to-video generation with motion-style controls through the PoYo generate endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative automation users use this skill to prepare PoYo Grok Imagine video-generation requests, submit authenticated payloads, and track returned task IDs for text-to-video or image-to-video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation prompts, image URLs, callback URLs, and related task data are sent to PoYo.

Mitigation: Use the skill only when sharing that task data with PoYo is acceptable, and avoid including sensitive content in prompts, image URLs, or callback data.

Risk: The PoYo API key can be exposed through shell history, logs, or process telemetry if passed as a command-line argument.

Mitigation: Set POYO_API_KEY as a protected environment variable and rotate the key if it may have been exposed.

## Reference(s):

- [PoYo Grok Imagine Model Page](https://poyo.ai/models/grok-imagine)
- [PoYo Grok Imagine API Docs](https://docs.poyo.ai/api-manual/video-series/grok-imagine)
- [PoYo Grok Imagine OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/grok-imagine.json)
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status)
- [Local API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-grok-imagine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the chosen model id, request payload or parameter summary, reference-image status, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
