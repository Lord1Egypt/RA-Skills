## Description:

Configures local Whisper speech recognition with whisper.cpp to convert voice messages from Feishu, Telegram, and similar channels into text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[279458179](https://clawhub.ai/user/279458179)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up offline speech-to-text on Linux servers for Chinese and multilingual voice messages. It provides installation, model selection, audio conversion, transcription, troubleshooting, and quantization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run mutable external code without version or integrity checks.

Mitigation: Pin whisper.cpp to a known commit or release and verify model checksums where possible before use.

Risk: Voice messages may contain sensitive information and temporary audio files can persist after transcription.

Mitigation: Avoid running downloaded scripts as root and delete temporary audio files after transcription, especially for sensitive messages.

## Reference(s):

- [whisper.cpp](https://github.com/ggml-org/whisper.cpp)
- [ClawHub skill page](https://clawhub.ai/279458179/skills/openclaw-whisper-asr)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for installing dependencies, building whisper.cpp, converting audio, running transcription, and quantizing models.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
