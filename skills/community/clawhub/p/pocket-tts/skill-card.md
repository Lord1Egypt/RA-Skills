## Description:

Generate English speech locally on CPU with Pocket TTS using built-in voices or a user-provided voice sample.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sherajdev](https://clawhub.ai/user/sherajdev)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add local English text-to-speech generation, voice selection, and optional voice cloning to workflows without relying on a hosted TTS API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing dependencies and first model or voice downloads may introduce unreviewed packages or remote assets.

Mitigation: Install in an isolated Python environment and pin or review package versions and downloaded assets before use.

Risk: Voice cloning can reproduce a person's voice from a WAV sample.

Mitigation: Use voice cloning only for voices the user has permission to reproduce and keep consent records where required.

Risk: The model is gated and requires accepting external model terms before generation succeeds.

Mitigation: Confirm Hugging Face model license acceptance and applicable terms before deployment.

## Reference(s):

- [Pocket TTS ClawHub Page](https://clawhub.ai/sherajdev/skills/pocket-tts)
- [Kyutai Pocket TTS Demo](https://kyutai.org/tts)
- [Pocket TTS GitHub Repository](https://github.com/kyutai-labs/pocket-tts)
- [Pocket TTS Hugging Face Model](https://huggingface.co/kyutai/pocket-tts)
- [Pocket TTS Paper](https://arxiv.org/abs/2509.06926)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and Python snippets; generated speech is saved as WAV audio when the CLI is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports built-in voice names, speech speed, output path, and an optional WAV voice sample for cloning.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
