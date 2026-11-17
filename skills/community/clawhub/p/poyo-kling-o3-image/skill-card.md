## Description:

Kling O3 image generation and editing on PoYo / poyo.ai via https://api.poyo.ai/api/generate/submit for prompt-only generation, reference-image editing, resolution and aspect-ratio selection, polling, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo Kling O3 image generation or image editing jobs, then guide polling or webhook follow-up for asynchronous results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY may be exposed if pasted into chat, browser code, frontend bundles, logs, screenshots, or public repositories.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and redact it from all shared output.

Risk: Prompts, reference image URLs, and callback URLs are sent to PoYo when a task is submitted.

Mitigation: Submit only data the user is willing to share with PoYo and the callback receiver; avoid confidential prompts, private image URLs, or private callback URLs unless those services are trusted.

Risk: The helper can make live PoYo API submissions when invoked with a prepared payload.

Mitigation: Make live API calls only after explicit user approval from a trusted server-side shell, then report and retain the returned task_id for polling.

## Reference(s):

- [PoYo Kling O3 Image Model Page](https://poyo.ai/models/kling-o3-image)
- [PoYo Kling O3 API Docs](https://docs.poyo.ai/api-manual/image-series/kling-o3)
- [PoYo API Key Page](https://poyo.ai/dashboard/api-key)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o3-image)
- [Local API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, request type, payload summary, resolution, aspect ratio, output format, image count, reference-image notes, task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
