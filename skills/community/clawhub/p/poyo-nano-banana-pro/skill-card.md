## Description:

Poyo Nano Banana Pro helps agents prepare PoYo Nano Banana Pro image generation and editing requests for text-to-image, image editing, multi-reference workflows, output format control, and 1K/2K/4K outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure, prepare, and optionally submit PoYo Nano Banana Pro image generation or editing jobs, including production-oriented payloads, polling, and webhook guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API requests can send prompts, image URLs, callback URLs, or other sensitive workflow data to a hosted third-party service.

Mitigation: Review payloads before submission and avoid including private prompts, private image URLs, callback URLs, or other sensitive data unless the user accepts sending them to PoYo.

Risk: The skill requires a PoYo API key.

Mitigation: Store POYO_API_KEY only in server-side environment variables or a secret manager, and do not expose it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Live submissions may create external API activity.

Mitigation: Submit requests only when the user explicitly asks and provides a safe server-side environment.

## Reference(s):

- [PoYo Nano Banana Pro API Reference](references/api.md)
- [PoYo Nano Banana Pro model page](https://poyo.ai/models/nano-banana-2-api)
- [PoYo Nano Banana Pro API docs](https://docs.poyo.ai/api-manual/image-series/nano-banana-2)
- [Poyo Nano Banana Pro on ClawHub](https://clawhub.ai/coolhackboy/skills/poyo-nano-banana-pro)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payloads and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, request payloads, curl commands, task IDs, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
