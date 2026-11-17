## Description:

OpenClaw Feishu Voice Free adds local voice-message transcription and speech synthesis for Feishu conversations using Whisper ASR and Qwen3-TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuaishi1991](https://clawhub.ai/user/shuaishi1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add Feishu voice-chat workflows that transcribe incoming voice messages, generate agent replies, and return synthesized speech through local ASR and TTS services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded credentials or tokens may be present in configuration examples.

Mitigation: Replace and rotate all embedded credentials before installation or reuse.

Risk: Local ASR and TTS services may be exposed without authentication or request limits.

Mitigation: Bind services to 127.0.0.1 and add authentication, request limits, and network access controls.

Risk: Persistence examples run services as root.

Mitigation: Run the services under a dedicated unprivileged account and avoid the root systemd units as written.

Risk: Voice cloning and automatic voice-message processing can create consent and misuse concerns.

Mitigation: Use only trusted voice clone files and require consent for voice cloning or automatic voice-message processing.

Risk: Unsafe file handling could expose or overwrite unintended media or voice-clone files.

Mitigation: Restrict accessible paths and review file permissions for audio input, generated output, and clone embedding files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuaishi1991/skills/openclaw-feishu-voice-free)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)
- [Whisper](https://github.com/openai/whisper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON and shell command snippets; runtime services return JSON transcription text and generated audio responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local model files, local HTTP ASR/TTS services, OpenClaw configuration, and Feishu channel setup.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
