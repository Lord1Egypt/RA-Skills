## Description:

Local Whisper speech-to-text for audio files and inbound voice notes on the OpenClaw Gateway host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabyaghosh](https://clawhub.ai/user/sabyaghosh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and run local Whisper transcription for audio files, WhatsApp voice notes, Telegram voice notes, and other inbound audio attachments on an OpenClaw Gateway host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer modifies the user-level Python environment and command path.

Mitigation: Run it in a dedicated virtual environment or disposable host before installing on a shared gateway.

Risk: The installer downloads unpinned dependencies.

Mitigation: Pin and hash dependencies before operational deployment.

Risk: The installer may overwrite common ~/.local/bin/whisper or ~/.local/bin/ffmpeg launchers.

Mitigation: Check for existing launchers before running the installer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sabyaghosh/skills/openclaw-whisper-voice)
- [PyTorch CPU Wheel Index](https://download.pytorch.org/whl/cpu)
- [Python Packaging get-pip Bootstrap](https://bootstrap.pypa.io/get-pip.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription wrapper can emit plain transcript text for agent workflows or txt, srt, vtt, and json files for standalone use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
