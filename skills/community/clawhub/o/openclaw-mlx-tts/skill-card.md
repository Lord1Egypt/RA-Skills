## Description: <br>
Provides local text-to-speech generation with mlx-audio, supporting multiple languages and models without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli-2025](https://clawhub.ai/user/gandli-2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate speech audio from text on local Apple Silicon systems, inspect TTS service status, reload TTS configuration, and choose supported mlx-audio models for multilingual synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The mlx-audio dependency and selected model IDs may download large third-party models and store them locally. <br>
Mitigation: Review the dependency and model IDs before installation or first use. <br>
Risk: The local TTS service and generated audio outputs may remain available beyond the immediate task. <br>
Mitigation: Enable the local TTS service only when needed and keep generated audio outputs within the documented safe directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gandli-2025/openclaw-mlx-tts) <br>
- [Publisher profile](https://clawhub.ai/user/gandli-2025) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local TTS actions that can produce audio files under /tmp or ~/.openclaw/voice/outputs/.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
