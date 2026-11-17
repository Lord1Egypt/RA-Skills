## Description:

Restores an OpenClaw Telegram voice-messaging setup by reinstalling local faster-whisper voice helpers and documenting the Microsoft TTS configuration needed after upgrades or rebuilds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenredmond-straiteis](https://clawhub.ai/user/stephenredmond-straiteis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to recover OpenClaw Telegram voice note transcription and outbound audio replies after an upgrade, rebuild, or provider-registration failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports serious unsafe execution concerns and advises against running the skill as root or against untrusted audio paths.

Mitigation: Review and fix the command-execution and temporary-file handling issues before installation, and run only with least-privilege permissions.

Risk: The server security guidance notes network downloads and hosted Edge/Microsoft TTS behavior that may send synthesis text to a remote service.

Mitigation: Pin and review dependencies before installation, and avoid sending sensitive text through the hosted TTS path unless that data flow is acceptable.

Risk: The evidence identifies local caching of generated audio as a behavior users should review.

Mitigation: Treat generated audio cache files as potentially sensitive and define retention, access, and cleanup controls before use.

Risk: The server security guidance says the expected transcribe-audio artifact is missing.

Mitigation: Resolve the missing artifact and confirm the installed transcription command exists before relying on the recovery workflow.

## Reference(s):

- [Recovery Notes](references/recovery-notes.md)
- [Voice Models Reference](references/voice_models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install local helper scripts, Python packages, runtime directories, and cached generated audio when executed.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
