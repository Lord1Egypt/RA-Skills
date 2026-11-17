## Description:

Transcribes audio files to text for OpenClaw using local Whisper-compatible speech recognition with Chinese language support and no API key requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxuebin20260309](https://clawhub.ai/user/liuxuebin20260309)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn voice messages or audio files into text, especially for Chinese speech-to-text workflows that should run locally after setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guide creates a wrapper that interpolates file paths and options into inline Python.

Mitigation: Review and preferably revise the wrapper to use safe argument passing before installation or deployment.

Risk: The setup downloads models from external endpoints even though inference is described as local.

Mitigation: Pin and verify model downloads, and treat local operation as applying after dependencies and models are installed.

Risk: The guide can modify the user's shell profile and add a persistent global whisper command.

Mitigation: Install in a controlled environment and change shell startup files only when a persistent PATH update is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuxuebin20260309/skills/lx-whisper-transcribe)
- [Hugging Face](https://huggingface.co)
- [HF Mirror](https://hf-mirror.com)
- [whisper.cpp tiny model mirror](https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and plain-text transcription output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription quality depends on installed dependencies, selected model size, language setting, audio quality, and model availability.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
