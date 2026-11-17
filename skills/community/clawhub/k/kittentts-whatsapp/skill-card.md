## Description:

WhatsApp voice notes via KittenTTS; it converts KittenTTS 24 kHz WAV output to WhatsApp-compatible 16 kHz OGG Opus using ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lakshibro](https://clawhub.ai/user/lakshibro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate WhatsApp-ready voice note audio from text with KittenTTS and ffmpeg. It also includes an optional transcription helper for incoming WhatsApp audio when Whisper is installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance can modify the system Python and package environment.

Mitigation: Use a virtual environment where possible, pin and verify dependencies, and avoid --break-system-packages on managed systems.

Risk: Runtime scripts may be unsafe for untrusted text or audio inputs until input handling and temporary-file behavior are reviewed.

Mitigation: Do not run the scripts as root, process trusted inputs only, and review the heredoc and temporary-file handling before broader deployment.

Risk: The first TTS run downloads a model from Hugging Face, which can fail or expose token-handling choices.

Mitigation: Pre-fetch approved models in controlled environments and avoid persisting HF_TOKEN in shell startup files unless that persistence is acceptable.

## Reference(s):

- [KittenTTS WhatsApp ClawHub page](https://clawhub.ai/lakshibro/skills/kittentts-whatsapp)
- [KittenML models on Hugging Face](https://huggingface.co/KittenML)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and script-driven audio file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates an OGG Opus voice note at /tmp/kittentts-walkie/walkie_reply.ogg and may print transcription text when the optional Whisper helper is used.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
