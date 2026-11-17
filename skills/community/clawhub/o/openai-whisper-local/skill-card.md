## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingchiu](https://clawhub.ai/user/wingchiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local users use this skill to transcribe or translate audio files with the Whisper CLI without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill requires adding the Homebrew openai-whisper CLI and allowing Whisper to download and cache model files locally.

Mitigation: Install only in environments where that CLI dependency and local model cache are acceptable.

Risk: Whisper processes the audio file paths supplied in generated commands.

Mitigation: Review file paths and audio contents before running transcription or translation commands.

## Reference(s):

- [OpenAI Whisper Research Page](https://openai.com/research/whisper)
- [ClawHub Skill Page](https://clawhub.ai/wingchiu/skills/openai-whisper-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
