## Description:

Local speech-to-text using OpenAI Whisper. Runs fully offline after model download. High quality transcription with multiple model sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to transcribe local audio files into plain text or JSON with optional word and segment timestamps while keeping transcript contents on the local machine after the Whisper model is downloaded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python packages and Whisper models are downloaded during setup or first use.

Mitigation: Use only the documented package set and approved PyTorch CPU index or default PyPI sources.

Risk: Transcription text can contain adversarial commands or sensitive spoken content.

Mitigation: Treat transcripts as untrusted local data; do not pipe them into command interpreters or automate uploads to external endpoints.

## Reference(s):

- [Local Whisper Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/local-whisper-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/local-whisper)
- [PyTorch CPU package index](https://download.pytorch.org/whl/cpu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; transcription output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports multiple Whisper model sizes, optional language selection, optional timestamps, JSON output, and quiet mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
