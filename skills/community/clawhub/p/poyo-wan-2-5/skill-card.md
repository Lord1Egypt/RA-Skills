## Description:

Wan 2.5 video generation helper for PoYo that prepares text-to-video or image-to-video payloads, submits asynchronous generation tasks, and guides polling or webhook follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build and submit PoYo Wan 2.5 text-to-video or image-to-video jobs with the correct model ID, payload fields, duration, size or resolution, and follow-up workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys can be exposed if placed in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid printing secrets in generated commands or responses.

Risk: Confidential prompts, private image URLs, callback URLs, or generated media links may be shared with PoYo or a webhook receiver during task submission.

Mitigation: Submit sensitive inputs only after confirming the user trusts PoYo and the callback receiver; otherwise redact or avoid those values.

Risk: Live task submission can trigger hosted video generation and return task identifiers that need follow-up handling.

Mitigation: Make live API calls only when explicitly requested from a trusted shell, then report the returned task_id and advise polling or webhook follow-up.

## Reference(s):

- [PoYo Wan 2.5 Model Page](https://poyo.ai/models/wan-2-5)
- [Wan 2.5 Text-to-Video API Docs](https://docs.poyo.ai/api-manual/video-series/wan2.5-text-to-video)
- [Wan 2.5 Image-to-Video API Docs](https://docs.poyo.ai/api-manual/video-series/wan2.5-image-to-video)
- [Local PoYo Wan 2.5 API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-wan-2-5)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model ID, request type, payload summary, submitted task_id, and next-step polling or webhook guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
