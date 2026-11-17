## Description:

Helps agents prepare, submit, and follow up on Sora 2 Pro Official video generation jobs through the PoYo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create PoYo Sora 2 Pro Official text-to-video or single-image-guided video requests, submit async tasks, and explain polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY can authorize external API requests if exposed.

Mitigation: Keep the key in server-side environment variables or a backend secret manager, and never place it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Prompts, source image URLs, and callback URLs are submitted to PoYo and may contain confidential information.

Mitigation: Review payloads before submission and avoid sending confidential prompts, private image URLs, or sensitive callback URLs unless PoYo and the callback receiver are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-sora-2-pro-official-api)
- [PoYo Sora 2 Official model page](https://poyo.ai/models/sora-2-official)
- [PoYo Sora 2 Pro Official API docs](https://docs.poyo.ai/api-manual/video-series/sora-2-pro-official)
- [Local PoYo API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash curl examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, request mode, payload summary, duration, aspect ratio, resolution, reference-image use, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
