## Description:

Liber SpeechAPI helps agents handle Telegram voice-message workflows, direct text-to-speech generation, and direct speech-to-text transcription through configured ASR and TTS service endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect agents to Liber SpeechAPI for voice-message handling, ASR transcription, and TTS generation, including Telegram-compatible OGG/Opus replies and optional voice cloning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio, text, and optional voice-clone samples may be sent to the configured Liber SpeechAPI backend.

Mitigation: Install only when the backend is trusted and prefer HTTPS for service communication.

Risk: Credential handling depends on environment variables and .env files readable by the skill.

Mitigation: Avoid using the bundled .env as production configuration and store only Liber-specific keys where this skill can read them.

Risk: Audio download behavior may need origin review before use with real credentials.

Mitigation: Review or patch the audio download origin check before deploying against sensitive services.

## Reference(s):

- [Liber SpeechAPI ClawHub listing](https://clawhub.ai/liberalchang/skills/liber-speechapi)
- [Liber SpeechAPI project documentation](https://github.com/liberalchang/Liber_SpeechAPI)
- [Liber SpeechAPI Reference](references/api.md)
- [Configuration](references/config.md)
- [Parameters](references/parameters.md)
- [Telegram/OpenClaw Workflow](references/workflow.md)
- [insanely-fast-whisper](https://github.com/Vaibhavs10/insanely-fast-whisper)
- [chatterbox](https://github.com/resemble-ai/chatterbox)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration, guidance]

**Output Format:** [Plain text, structured JSON, Markdown guidance, shell commands, and audio URLs or saved file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May shorten long replies for voice playback; direct ASR defaults to JSON and direct TTS defaults to WAV, while Telegram voice replies use OGG/Opus.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
