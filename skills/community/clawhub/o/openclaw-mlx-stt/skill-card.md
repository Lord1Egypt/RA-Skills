## Description: <br>
Runs local speech-to-text with mlx-audio Whisper on Apple Silicon to transcribe supported audio files without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli-2025](https://clawhub.ai/user/gandli-2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to transcribe local audio files, inspect STT service status, reload STT configuration, and choose models for multilingual speech recognition or translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files and transcripts may contain sensitive personal or business information. <br>
Mitigation: Run processing locally as documented, limit file access, and handle transcript storage and sharing under the user's data policy. <br>
Risk: The workflow depends on installing mlx-audio and selecting local speech models. <br>
Mitigation: Review and pin the third-party dependency and chosen models before deployment, then test transcription behavior in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gandli-2025/openclaw-mlx-stt) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with transcript text, detected language, duration, and timestamped segments; Markdown guidance with command and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local mlx-audio installation and configured OpenClaw STT service; no API key is documented.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
