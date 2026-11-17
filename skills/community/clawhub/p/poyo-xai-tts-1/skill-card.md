## Description:

Generate expressive multilingual speech on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `xai-tts-1`, text-to-speech, voice presets, language code, speech tags, output audio formats, async status polling, callbacks, and server-side integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare and submit PoYo xAI TTS 1 text-to-speech payloads, choose voice, language, output audio, callback, and polling options, and handle returned task identifiers. It is intended for explicit PoYo workflows that need server-side API-key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY is required to submit requests and could be exposed if used in client-side code, logs, screenshots, shared shells, or chat output.

Mitigation: Keep POYO_API_KEY in a server-side secret store or protected environment and avoid running the submission script on shared machines.

Risk: Submitted text, callback URLs, generated audio URLs, task ids, and authorization headers may contain sensitive workflow or user data.

Mitigation: Submit private text or callback URLs only when permitted by the PoYo account and applicable data handling policies, and avoid logging sensitive request or response fields.

Risk: The helper can make a live PoYo API submission when the script is run with a prepared payload.

Mitigation: Make live API calls only after the user explicitly requests submission and confirms the payload should be sent from a trusted server-side environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-xai-tts-1)
- [PoYo xAI TTS 1 model page](https://poyo.ai/models/xai-tts-1)
- [PoYo xAI TTS 1 API docs](https://docs.poyo.ai/api-manual/music-series/xai-tts-1)
- [PoYo xAI TTS 1 OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/xai-tts-1.json)
- [PoYo xAI TTS 1 API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads, curl examples, shell command guidance, and concise parameter summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id after an explicitly requested live submission.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
