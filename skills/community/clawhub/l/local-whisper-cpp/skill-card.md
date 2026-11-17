## Description:

Local speech-to-text using whisper-cli (whisper.cpp).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxxin](https://clawhub.ai/user/wuxxin)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to transcribe local audio files with whisper-cli and a locally installed large-v3-turbo whisper.cpp model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model setup may involve downloading a file into a system path, where source integrity and privileges matter.

Mitigation: Download the model as an unprivileged user when possible, verify the source and checksum if available, and avoid running setup commands with more privileges than necessary.

Risk: The transcription command runs locally against user-provided audio paths and optional whisper-cli arguments.

Mitigation: Use trusted local audio files, review any additional command options before execution, and keep whisper-cli on a trusted system path.

## Reference(s):

- [Local Whisper (cpp) on ClawHub](https://clawhub.ai/wuxxin/skills/local-whisper-cpp)
- [whisper.cpp large-v3-turbo model download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin?download=true)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text transcription and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires whisper-cli and a local model file at the configured path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
