## Description:

Mlx Tts helps agents generate local multilingual text-to-speech audio with mlx-audio on Apple Silicon, using selectable models and bounded output paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli-2025](https://clawhub.ai/user/gandli-2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to have an agent convert supplied text into local speech files, check TTS server status, reload configuration, and select models or languages for multilingual voice output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing mlx-audio with prereleases allowed can increase supply-chain review risk.

Mitigation: Review the package source and pin a trusted mlx-audio version before deployment.

Risk: Large TTS models can require substantial local memory and may download model files on first use.

Mitigation: Select a model that fits the target Apple Silicon machine and pre-warm or pre-download models before relying on the skill.

Risk: Generated audio should remain confined to approved local output locations.

Mitigation: Keep output paths within /tmp or ~/.openclaw/voice/outputs/ and retain symlink rejection checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gandli-2025/skills/openclaw-mlx-tts)
- [Publisher Profile](https://clawhub.ai/user/gandli-2025)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, configuration snippets, and audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio paths are limited to /tmp or ~/.openclaw/voice/outputs/; model size, first-run download time, and memory use vary by selected model.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
