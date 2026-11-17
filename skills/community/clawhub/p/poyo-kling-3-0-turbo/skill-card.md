## Description:

Kling 3.0 Turbo video generation on PoYo / poyo.ai via the PoYo async generation API, covering text-to-video, first-frame image-to-video, multi-shot storyboards, duration control, aspect ratios, polling, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare, submit, and follow up on PoYo Kling 3.0 Turbo video generation jobs, including text-to-video, first-frame image-to-video, and multi-shot storyboard workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY exposure could allow unauthorized use of the PoYo API.

Mitigation: Keep the key in server-side environment variables or a backend secret manager, and do not place it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Prompts, source image URLs, and callback URLs are sent to PoYo during generation workflows.

Mitigation: Avoid submitting confidential media, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

Risk: Live API submissions can create external tasks and may incur usage costs or expose payload data.

Mitigation: Make live API calls only when the user explicitly asks and the request is running from a safe server-side environment.

## Reference(s):

- [PoYo Kling 3.0 Turbo API Reference](references/api.md)
- [PoYo Kling 3.0 Turbo Model Page](https://poyo.ai/models/kling-3-0-turbo)
- [PoYo Kling 3.0 Turbo API Docs](https://docs.poyo.ai/api-manual/video-series/kling-3-0-turbo)
- [PoYo API Key Page](https://poyo.ai/dashboard/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the selected model id, request mode, payload summary or JSON, duration, aspect ratio, reference image status, returned task_id, and polling or webhook next step.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
