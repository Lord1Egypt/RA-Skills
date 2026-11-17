## Description:

Multi Edge Tts Cn generates Chinese text-to-speech audio with Edge-TTS voices and converts the result to messaging-friendly formats such as OGG/Opus and AMR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itian932](https://clawhub.ai/user/itian932)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn Chinese text into audio files for Feishu and WeCom voice-message workflows. It supports multiple Mandarin, Cantonese, and Taiwan voices plus tuned custom presets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that output path checks warn but do not enforce the documented whitelist, so a caller can write or overwrite arbitrary writable paths.

Mitigation: Use only explicit output paths under /tmp/openclaw or the documented OpenClaw media/workspace directories, and review generated paths before sending or storing files.

Risk: The installer may install dependencies into a system or privileged Python environment and does not pin the edge-tts dependency version during installation.

Mitigation: Install in a trusted, non-privileged virtual environment or user environment and pin or review dependency versions before routine use.

Risk: The skill requires network access to the Edge-TTS service, so synthesis can fail or retry when connectivity, authorization, or rate limits are encountered.

Mitigation: Run it only where outbound network use is acceptable, expect transient failures, and keep text inputs within the documented length and messaging-size limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itian932/skills/multi-edge-tts-cn)
- [Publisher profile](https://clawhub.ai/user/itian932)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Code, Configuration]

**Output Format:** [Audio files with a returned file path; documented CLI and Python API examples use Markdown with code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is an OGG file under /tmp/openclaw; supported extensions include .ogg, .opus, .amr, .mp3, .wav, .flac, and .aac, with AMR and OGG size checks documented for messaging channels.]

## Skill Version(s):

2.3.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
