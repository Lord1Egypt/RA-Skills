## Description:

Helps agents prepare and submit Kling 2.5 Turbo Pro video-generation tasks through the PoYo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create text-to-video, image-to-video, and first/last-frame Kling 2.5 Turbo Pro payloads, submit trusted JSON payloads to PoYo, and explain polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a PoYo API key to submit video-generation requests.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and do not expose it in browser code, logs, screenshots, repositories, or chat output.

Risk: Prompts, image URLs, callback URLs, and generated media URLs may contain private or sensitive information.

Mitigation: Submit only data that the user accepts PoYo and any webhook receiver handling, and review payload JSON before sending it.

Risk: The helper can make live API submissions when explicitly used with a prepared payload.

Mitigation: Make live calls only from a trusted shell after the user confirms the payload and intended PoYo workflow.

## Reference(s):

- [PoYo Kling 2.5 Turbo Pro Model Page](https://poyo.ai/models/kling-2-5-turbo-pro)
- [PoYo Kling 2.5 Turbo Pro API Documentation](https://docs.poyo.ai/api-manual/video-series/kling-2-5-turbo-pro)
- [Local API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-kling-2-5-turbo-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payload examples and optional curl or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a PoYo task_id after an explicit trusted submission; otherwise produces guidance and payloads only.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
