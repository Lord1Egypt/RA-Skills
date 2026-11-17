## Description:

Local STT and TTS on macOS using native Apple capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strrl](https://clawhub.ai/user/strrl)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to transcribe local audio files and generate spoken audio on macOS without cloud services or API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom TTS output path can overwrite audio files outside the intended outbound media folder.

Mitigation: Use the default output path, do not let untrusted content choose output_path, and restrict future output paths to ~/.openclaw/media/outbound with traversal and absolute-path checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/strrl/skills/macos-local-voice)
- [OpenClaw](https://openclaw.ai)
- [yap](https://github.com/finnvoor/yap)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text, file paths, and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on macOS; TTS writes AIFF or OGG audio files and STT writes transcripts to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
