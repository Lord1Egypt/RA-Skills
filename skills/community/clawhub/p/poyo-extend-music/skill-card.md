## Description:

Helps agents prepare PoYo Extend Music payloads, curl commands, and follow-up status retrieval guidance for extending an existing track from an audio_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure PoYo music-extension requests, choose simple or custom continuation settings, prepare safe server-side submissions, and retrieve task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if used in browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and redact authorization headers from logs and user-visible output.

Risk: Payloads may send private prompts, audio identifiers, callback URLs, or generated URLs to PoYo.

Mitigation: Review the JSON payload before submission and send only content that is appropriate for PoYo to process.

Risk: Live submissions create external PoYo tasks and may incur provider-side processing.

Mitigation: Make live API calls only after explicit user confirmation from a trusted server-side shell.

## Reference(s):

- [PoYo Extend Music API Reference](references/api.md)
- [PoYo Extend Music model page](https://poyo.ai/models/extend-music)
- [PoYo Extend Music API docs](https://docs.poyo.ai/api-manual/music-series/extend-music)
- [PoYo Extend Music OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/extend-music.json)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-extend-music)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live submissions require curl, POYO_API_KEY, a prepared payload file, and explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
