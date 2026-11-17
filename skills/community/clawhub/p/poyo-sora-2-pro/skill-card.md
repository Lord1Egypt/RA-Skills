## Description:

Use PoYo AI Sora 2 Pro for longer premium video generation through the https://api.poyo.ai/api/generate/submit endpoint, including 15s or 25s clips, storyboard control, style presets, image-to-video input, and payloads for sora-2-pro or sora-2-pro-private.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare, submit, and track PoYo Sora 2 Pro video generation jobs with authenticated API calls, documented model IDs, and clear polling or webhook follow-up steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script allows passing a PoYo API key as a command-line argument, which can expose the credential locally.

Mitigation: Set POYO_API_KEY through a protected environment or secret mechanism, avoid passing the key on the command line, and rotate any key already used that way.

Risk: Using the skill sends generation prompts, reference image URLs, and optional callback information to PoYo.

Mitigation: Review prompts, image URLs, and callback destinations before submission and use the skill only when sharing that data with PoYo is intended.

## Reference(s):

- [PoYo Sora 2 Pro API Reference](references/api.md)
- [PoYo Sora 2 Pro model page](https://poyo.ai/models/sora-2-pro)
- [PoYo Sora 2 Pro API docs](https://docs.poyo.ai/api-manual/video-series/sora-2-pro)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [PoYo Sora 2 Pro OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/sora-2-pro.json)
- [ClawHub release page](https://clawhub.ai/coolhackboy/skills/poyo-sora-2-pro)
- [Publisher profile](https://clawhub.ai/user/coolhackboy)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model ID, concise parameter summary, reference-image involvement, returned task_id, and polling or webhook next step.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
