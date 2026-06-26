## Description: <br>
Local text-to-speech using Qwen3-TTS with mlx_audio on macOS Apple Silicon or qwen-tts on Linux and Windows for privacy-first offline multilingual speech synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irachex](https://clawhub.ai/user/irachex) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up local Qwen3-TTS workflows, choose macOS or Linux/Windows backends, and generate speech without sending text to a cloud TTS provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Realistic voice cloning can be used without consent or for impersonation. <br>
Mitigation: Use voice cloning only for your own voice or voices where you have explicit permission, and do not use it for impersonation, fraud, harassment, or deceptive content. <br>
Risk: Local ML setup depends on external model downloads and Python audio/ML packages. <br>
Mitigation: Install only in environments where local ML dependencies and external model downloads are acceptable, and review dependencies before deployment. <br>


## Reference(s): <br>
- [macOS mlx_audio Reference](references/macos_mlx_audio.md) <br>
- [Linux/Windows qwen-tts Reference](references/linux_windows_transformers.md) <br>
- [Privacy & Security Benefits of Local TTS](references/privacy_security.md) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wrapper scripts can produce local WAV audio files when run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
