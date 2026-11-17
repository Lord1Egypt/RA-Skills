## Description:

Gipformer ASR transcribes Vietnamese speech from WAV, FLAC, OGG, MP3, and M4A audio using a 65M-parameter Zipformer-RNNT model with server-side VAD chunking and batching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-ggroup](https://clawhub.ai/user/ai-ggroup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run a local Vietnamese speech-to-text service and transcribe audio files through a CLI or HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local transcription service is unauthenticated and may be unsafe to expose beyond localhost.

Mitigation: Keep it bound to 127.0.0.1 unless authentication, request-size limits, duration limits, and rate or concurrency controls are added.

Risk: The skill downloads Python packages and remote model files before inference.

Mitigation: Install only when the dependency and model sources are trusted and reviewed for the intended environment.

Risk: Submitted audio is decoded and transcribed by the local server process.

Mitigation: Avoid submitting sensitive audio unless the deployment environment and data-handling requirements have been reviewed.

## Reference(s):

- [Gipformer ASR Server API Reference](artifact/references/api.md)
- [Gipformer ASR ClawHub Page](https://clawhub.ai/ai-ggroup/skills/gipformer)
- [Gipformer 65M RNNT Hugging Face Model](https://huggingface.co/g-group-ai-lab/gipformer-65M-rnnt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transcripts and per-chunk timing metadata when used with the included server and client scripts.]

## Skill Version(s):

1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
