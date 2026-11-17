## Description:

Local speech-to-text using OpenAI Whisper. Runs fully offline after model download. High quality transcription with multiple model sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araa47](https://clawhub.ai/user/araa47)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe local audio files with OpenAI Whisper, choosing model size, language, timestamp, JSON, and quiet-mode options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial dependency and model downloads can be large and may vary over time.

Mitigation: Install as an unprivileged user and pin or review package versions when reproducible or tightly controlled installs are required.

Risk: Audio inputs and generated transcripts may contain sensitive spoken content.

Mitigation: Process only authorized local audio files and review transcripts before sharing or storing them outside the local environment.

## Reference(s):

- [Local Whisper ClawHub release](https://clawhub.ai/araa47/skills/local-whisper)
- [PyTorch CPU wheel index](https://download.pytorch.org/whl/cpu)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text transcript or JSON with optional language and segment timestamps; setup and usage guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally after the initial Whisper model download; supports model, language, timestamps, JSON, and quiet-mode options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
