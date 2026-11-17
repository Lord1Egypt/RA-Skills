## Description:

Prepares and submits PoYo Gemini 3.1 Flash TTS text-to-speech requests, including payload guidance for voices, style instructions, two-speaker dialogue, output formats, callbacks, and task status retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare PoYo Gemini 3.1 Flash TTS speech payloads, submit trusted requests from a server-side shell, and retrieve asynchronous task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys or request data could be exposed through browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid logging private scripts, customer text, callback URLs, task IDs, or generated audio URLs unless policy allows it.

Risk: The skill can submit user-prepared speech requests to PoYo when explicitly used.

Mitigation: Review payloads before submission and make live API calls only from a trusted server-side environment after the user explicitly requests execution.

## Reference(s):

- [PoYo Gemini 3.1 Flash TTS model page](https://poyo.ai/models/gemini-3-1-flash-tts)
- [PoYo Gemini 3.1 Flash TTS API docs](https://docs.poyo.ai/api-manual/music-series/gemini-3-1-flash-tts)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [PoYo Gemini 3.1 Flash TTS API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, speaker mode, voice presets, style instructions, request payloads, task IDs, and task-status next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
