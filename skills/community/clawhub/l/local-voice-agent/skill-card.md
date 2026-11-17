## Description:

Complete offline voice-to-voice AI assistant for OpenClaw (Whisper.cpp STT + Pocket-TTS). 100% local processing, no cloud APIs, no costs. Use for hands-free operation, voice commands, accessibility, or custom voice cloning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinological](https://clawhub.ai/user/pinological)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add local speech-to-text, AI response handling, and text-to-speech workflows for hands-free commands, voice notes, accessibility, and interactive voice conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe configuration, network, and dependency practices may expose local voice workflows to avoidable security risk.

Mitigation: Review and harden the skill before installation, remove shell eval usage, pin downloaded dependencies and models, and keep the TTS service bound to localhost.

Risk: Remote or untrusted TTS endpoints can receive text derived from voice commands or transcriptions.

Mitigation: Use a trusted local Pocket-TTS service by default and only configure remote HTTP TTS endpoints after explicit trust review.

Risk: Microphone recordings, transcriptions, generated speech, and cached outputs can contain sensitive local data.

Mitigation: Treat local audio artifacts and caches as sensitive data, limit file access, and clear caches or temporary recordings when no longer needed.

Risk: The skill's privacy and completeness claims may be overstated for deployments that use remote services or incomplete local setup.

Mitigation: Confirm the actual runtime configuration, installed dependencies, and service endpoints before relying on offline-processing claims.

## Reference(s):

- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Discord](https://discord.com/invite/clawd)
- [ClawHub Skill Page](https://clawhub.ai/pinological/skills/local-voice-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and generated text or audio-file paths from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can transcribe local audio, send text through an OpenClaw workflow, request speech synthesis from a configured Pocket-TTS service, and cache local audio-derived outputs when enabled.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
