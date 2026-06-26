## Description: <br>
Local TTS/STT integration for OpenClaw using mlx-audio - Zero API keys, Zero cloud dependency <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli-2025](https://clawhub.ai/user/gandli-2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run local speech synthesis, transcription, status checks, and model selection on Apple Silicon systems without sending text or audio to cloud APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make host-level dependency changes and includes unverified installer execution. <br>
Mitigation: Review install.sh before running it, install dependencies manually where possible, and avoid curl-to-shell installation paths unless the source and command are acceptable for the environment. <br>
Risk: Local text, audio, and generated outputs may appear in logs or temporary files during audio processing. <br>
Mitigation: Use non-sensitive text and audio unless local logging and temporary output handling are acceptable, and clean generated files after use. <br>
Risk: Voice cloning can misuse audio from people who have not granted permission. <br>
Mitigation: Use only voice samples that the user owns or has explicit permission to clone. <br>
Risk: Autonomous-code workflow documentation is bundled with the package and may be unrelated to normal audio use. <br>
Mitigation: Treat the autonomous workflow files as documentation, not runtime requirements, and review any automation scripts before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gandli-2025/openclaw-mlx-audio) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Audio files, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON tool results, command text, and local MP3 or WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local mlx-audio CLI commands, writes generated speech to caller-provided or temporary paths, and returns transcription text from local audio files.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release metadata; artifact frontmatter lists 0.2.0 and package.json lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
