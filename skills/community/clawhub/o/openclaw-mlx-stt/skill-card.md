## Description:

Mlx Stt transcribes local audio files to text with mlx-audio Whisper models on Apple Silicon, supporting language detection, timestamps, and optional translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli-2025](https://clawhub.ai/user/gandli-2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run local speech-to-text transcription for provided audio files without external API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step allows prerelease versions of the third-party mlx-audio package.

Mitigation: Verify the package source before installation and pin an exact reviewed version for repeatable deployments.

Risk: The skill reads user-provided audio files and processes them through local speech-to-text components.

Mitigation: Review file paths and local data-handling expectations before processing sensitive audio.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gandli-2025/skills/openclaw-mlx-stt)
- [Publisher profile](https://clawhub.ai/user/gandli-2025)

## Skill Output:

**Output Type(s):** [text, json, configuration, shell commands, guidance]

**Output Format:** [JSON tool responses and Markdown guidance with shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns transcript text, detected language, duration, and timestamped segments when transcription succeeds.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
