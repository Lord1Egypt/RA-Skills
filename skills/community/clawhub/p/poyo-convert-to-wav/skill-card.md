## Description:

Convert generated music tracks to WAV on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `convert-to-wav`, WAV export from a completed music task_id plus audio_id, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare PoYo Convert to WAV payloads, submit trusted server-side conversion requests, configure callbacks, and retrieve conversion status for completed PoYo music tracks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if used in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in a trusted server-side environment or secret manager and avoid echoing authorization headers.

Risk: Task IDs, audio IDs, callback URLs, generated URLs, and private prompts may contain sensitive project or customer information.

Mitigation: Review payload files before submission and keep private identifiers and generated URLs out of logs unless product policy allows it.

Risk: Submitting a conversion request to PoYo sends user-prepared data to an external service.

Mitigation: Make live API calls only after the user explicitly confirms the payload should be sent from a trusted server-side shell.

## Reference(s):

- [PoYo Convert to WAV API Reference](artifact/references/api.md)
- [PoYo Convert to WAV Model Page](https://poyo.ai/models/convert-to-wav)
- [PoYo Convert to WAV API Docs](https://docs.poyo.ai/api-manual/music-series/convert-to-wav)
- [PoYo Convert to WAV OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/convert-to-wav.json)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-convert-to-wav)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a submitted PoYo task_id when the user explicitly asks to send a prepared request from a trusted server-side environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
