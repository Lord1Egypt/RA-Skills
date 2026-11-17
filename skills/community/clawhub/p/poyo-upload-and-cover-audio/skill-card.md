## Description:

Transform uploaded audio into a new music style on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `upload-and-cover-audio`, audio cover generation, style transformation, custom mode, instrumental output, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo Upload and Cover Audio payloads, choose simple or custom mode, submit confirmed audio transformation requests, and retrieve results through callbacks or music detail lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys can be exposed if copied into browser code, logs, screenshots, repositories, or chat output.

Mitigation: Store POYO_API_KEY only in server-side environment variables or a backend secret manager, and redact authorization headers from user-facing output.

Risk: Payloads may send private audio URLs, lyrics, customer data, callback URLs, task ids, or generated result URLs to PoYo or to logs.

Mitigation: Review payload JSON before submission and avoid logging sensitive URLs or content unless the product policy and workflow explicitly allow it.

Risk: Live submissions create external asynchronous generation tasks with PoYo.

Mitigation: Submit only after the user explicitly confirms the payload and intends to use PoYo for the audio cover workflow.

## Reference(s):

- [PoYo Upload and Cover Audio API Reference](references/api.md)
- [PoYo Upload and Cover Audio model page](https://poyo.ai/models/upload-and-cover-audio)
- [PoYo Upload and Cover Audio API docs](https://docs.poyo.ai/api-manual/music-series/upload-and-cover-audio)
- [PoYo Upload and Cover Audio OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/upload-and-cover-audio.json)
- [PoYo query music detail docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo music webhook docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-upload-and-cover-audio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id after a confirmed live submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
