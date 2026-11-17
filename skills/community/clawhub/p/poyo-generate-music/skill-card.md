## Description:

Generate Music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `generate-music`, AI music generation, background tracks, soundtrack drafts, instrumental songs, custom mode, music callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo music-generation payloads, choose simple or custom mode, submit async generation tasks, and retrieve or route generated music results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API credentials could be exposed if used in browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid echoing it in generated commands or logs.

Risk: Payload files may contain private lyrics, prompts, callback URLs, or generated audio URLs.

Mitigation: Review JSON payloads before submission and avoid logging sensitive prompts, callback URLs, or generated asset URLs unless policy allows it.

Risk: Callback URLs can send task events to unintended recipients if they are not controlled by the user.

Mitigation: Use callback URLs only on trusted HTTPS endpoints the user controls.

## Reference(s):

- [PoYo Generate Music API Reference](references/api.md)
- [PoYo Generate Music model page](https://poyo.ai/models/generate-music)
- [PoYo Generate Music API docs](https://docs.poyo.ai/api-manual/music-series/generate-music)
- [PoYo Music Detail API docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo Music Webhook docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-generate-music)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown with JSON payloads and inline bash or curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a chosen model id, generation mode, instrumental or vocal intent, final payload or parameter summary, returned task_id, and next retrieval or webhook step.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
