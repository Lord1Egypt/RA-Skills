## Description:

Helps agents prepare, submit, and follow up on Kling O3 video generation jobs through PoYo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Kling O3 text-to-video, image-to-video, reference-to-video, and multi-shot requests, then submit jobs and explain polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source image URLs, reference image URLs, generated-video job data, and callback URLs are sent to PoYo.

Mitigation: Use the skill only when PoYo is acceptable for that data, avoid confidential media or prompts, and use callback URLs only for trusted HTTPS endpoints you control.

Risk: POYO_API_KEY can authorize video-generation API requests if exposed.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid placing it in browser code, public repositories, logs, screenshots, or chat output.

## Reference(s):

- [PoYo Kling O3 API Reference](references/api.md)
- [PoYo Kling O3 model page](https://poyo.ai/models/kling-o3-api)
- [PoYo Kling O3 API docs](https://docs.poyo.ai/api-manual/video-series/kling-o3)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o3)
- [Publisher profile](https://clawhub.ai/user/coolhackboy)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, request type, payload details, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
