## Description:

Grok Imagine Video 1.5 image-to-video generation on PoYo / poyo.ai via https://api.poyo.ai/api/generate/submit; use for grok-imagine-video-1.5, one source image, prompt-driven motion, 480p or 720p output, duration control, polling, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo Grok Imagine Video 1.5 image-to-video jobs from one source image, then guide polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY can grant access to PoYo API usage if exposed.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager, and do not place it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Payloads may contain confidential prompts, private source image URLs, or private callback URLs.

Mitigation: Review the JSON payload before submission and avoid sending confidential prompts, private image URLs, or private callback URLs unless PoYo and the callback receiver are trusted.

Risk: Running the submit script sends a live image-to-video generation request to PoYo.

Mitigation: Run the script only when the user explicitly requests submission and provides a reviewed payload in a trusted shell.

## Reference(s):

- [PoYo Grok Imagine Video 1.5 API Reference](references/api.md)
- [PoYo Grok Imagine Video 1.5 model page](https://poyo.ai/models/grok-imagine-video-1-5)
- [PoYo Grok Imagine Video 1.5 API docs](https://docs.poyo.ai/api-manual/video-series/grok-imagine-video-1-5)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-grok-imagine-video-1-5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id and next-step polling or webhook guidance after a live submission.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
