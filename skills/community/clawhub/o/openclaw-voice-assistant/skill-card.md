## Description:

Windows voice companion for OpenClaw with Porcupine wake word detection, local faster-whisper speech-to-text, OpenClaw Gateway WebSocket responses, ElevenLabs text-to-speech, multi-turn follow-up listening, mic suppression, and system tray controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurtivy](https://clawhub.ai/user/kurtivy)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to run a Windows voice assistant that listens for a wake word or hotkey, transcribes speech locally, sends text to an OpenClaw gateway, and plays spoken responses. It also helps configure wake words, voice selection, silence thresholds, and generated chime or thinking sounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assistant handles live microphone input and may capture sensitive speech during wake-word or follow-up listening.

Mitigation: Install only if always-on local listening is acceptable, pause or quit the tray app when not needed, and avoid speaking sensitive information while logging is enabled.

Risk: Gateway, ElevenLabs, and Picovoice credentials are stored in local environment configuration.

Mitigation: Treat the .env file as secret material, keep tokens out of shared logs and repositories, and rotate credentials if they may have been exposed.

Risk: A non-local or untrusted gateway endpoint could receive transcribed user speech.

Mitigation: Keep the gateway on the default local address unless a trusted secure endpoint is explicitly required and configured.

Risk: Unpinned dependencies can change behavior or introduce supply-chain exposure over time.

Mitigation: Use an isolated virtual environment and prefer pinned dependency versions before running the assistant in regular use.

## Reference(s):

- [Voice Assistant Architecture](references/architecture.md)
- [Voice Assistant Troubleshooting](references/troubleshooting.md)
- [Picovoice](https://picovoice.ai)
- [Picovoice Console](https://console.picovoice.ai/)
- [ClawHub Skill Page](https://clawhub.ai/kurtivy/skills/openclaw-voice-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Audio files, Guidance]

**Output Format:** [Markdown instructions with Python scripts, environment configuration, WebSocket text messages, and generated WAV audio assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, Python 3.10+, OpenClaw gateway credentials, ElevenLabs API credentials, Picovoice access key, microphone input, and speaker output.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
