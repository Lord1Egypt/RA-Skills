## Description:

Veo 3.1 Official video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `veo3.1-fast-official`, `veo3.1-lite-official`, `veo3.1-quality-official`, text-to-video, image-to-video, first/last-frame video, reference video, audio control, polling, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare, submit, and follow up on PoYo Veo 3.1 Official video-generation jobs, including text-to-video, image-guided, first/last-frame, reference-guided, polling, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PoYo API key could be exposed through browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid logging or displaying the key.

Risk: Prompts, source media URLs, or callback URLs may contain confidential information that would be sent to PoYo or a webhook receiver.

Mitigation: Review payload JSON before submission and avoid confidential prompts, private media URLs, or sensitive callback URLs unless the user trusts PoYo and the callback receiver.

Risk: A live request to PoYo may submit user-prepared video-generation payloads before they are ready.

Mitigation: Submit only when the user explicitly requests a live API call from a trusted shell, and report the returned task_id for follow-up polling or webhook handling.

## Reference(s):

- [PoYo Veo 3.1 Official API Reference](references/api.md)
- [PoYo Veo 3.1 Official Model Page](https://poyo.ai/models/veo-3-1-official)
- [PoYo Veo 3.1 Official API Docs](https://docs.poyo.ai/api-manual/video-series/veo-3-1-official)
- [PoYo API Key Page](https://poyo.ai/dashboard/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id when the user explicitly requests submission.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
