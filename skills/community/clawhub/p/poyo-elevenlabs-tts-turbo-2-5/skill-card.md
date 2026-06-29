## Description: <br>
Generate speech on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `elevenlabs-tts-turbo-2-5`, text-to-speech, voice selection, speech speed, stability, similarity boost, style, timestamps, language code, async task submission, callbacks, and task status retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo ElevenLabs TTS Turbo 2.5 request payloads, choose voice and delivery parameters, submit trusted server-side text-to-speech jobs, and explain task status retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys, customer text, callback URLs, task ids, or generated audio URLs may be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid logging private request or result data unless product policy explicitly allows it. <br>
Risk: A live submission sends text-to-speech content to the PoYo API and may affect production queues or callbacks. <br>
Mitigation: Make live API calls only when the user explicitly asks, provides a trusted server-side environment, and confirms the prepared payload. <br>
Risk: Model-specific options may change or be unsupported for a given request. <br>
Mitigation: Verify current field support in the PoYo documentation before relying on voice, timestamp, language, or delivery-control parameters. <br>


## Reference(s): <br>
- [PoYo ElevenLabs TTS Turbo 2.5 API Reference](references/api.md) <br>
- [PoYo ElevenLabs TTS Turbo 2.5 Documentation](https://docs.poyo.ai/api-manual/music-series/elevenlabs-tts-turbo-2-5) <br>
- [PoYo ElevenLabs TTS Turbo 2.5 Model Page](https://poyo.ai/models/elevenlabs-tts-turbo-2-5) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-elevenlabs-tts-turbo-2-5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash/curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, voice and language choices, changed delivery controls, a final payload or parameter summary, returned task_id, and the next retrieval step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
