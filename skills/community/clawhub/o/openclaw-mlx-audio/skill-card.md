## Description:

Local TTS/STT integration for OpenClaw using mlx-audio - Zero API keys, Zero cloud dependency

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli-2025](https://clawhub.ai/user/gandli-2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run local text-to-speech, speech-to-text, and voice-cloning workflows on Apple Silicon without cloud APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs mutable remote code and force-installs unpinned prerelease dependencies.

Mitigation: Review install.sh before execution and prefer pinned, trusted package-manager commands for uv and mlx-audio.

Risk: Cache-deletion troubleshooting commands can remove local Hugging Face model data.

Mitigation: Run cache cleanup only after reviewing the exact path and confirming the cached models can be safely removed.

Risk: Speech transcription and voice cloning can process sensitive or unauthorized audio.

Mitigation: Use the TTS, STT, and voice-cloning features only with audio the user is authorized to process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gandli-2025/skills/openclaw-mlx-audio)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with shell and JSON snippets; tool calls may return status data, audio file paths, or transcription text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for local macOS Apple Silicon workflows using OpenClaw, ffmpeg, uv, and mlx-audio.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
