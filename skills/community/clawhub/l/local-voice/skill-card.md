## Description: <br>
Local text-to-speech (TTS) and speech-to-text (STT) using FluidAudio on Apple Silicon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TrondW](https://clawhub.ai/user/TrondW) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up local voice capabilities on Apple Silicon Macs, including offline TTS, STT, and voice assistant integration through a localhost service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs a macOS LaunchAgent that starts a background local voice service at login. <br>
Mitigation: Review the setup script before running it, and unload the LaunchAgent and remove installed files when the service should be disabled. <br>
Risk: The service listens on a localhost HTTP port for TTS and STT requests. <br>
Mitigation: Keep the service bound to 127.0.0.1 and avoid exposing or proxying the endpoint to untrusted networks. <br>
Risk: Setup and first use may install Homebrew or Swift dependencies and download speech models. <br>
Mitigation: Install only in environments where those dependency and model downloads are acceptable, and review dependency sources before deployment. <br>


## Reference(s): <br>
- [Kokoro Voice Reference](references/VOICES.md) <br>
- [FluidAudio Swift package](https://github.com/FluidInference/FluidAudio.git) <br>
- [Hummingbird Swift package](https://github.com/hummingbird-project/hummingbird.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Swift, JavaScript, JSON, and XML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup and use of a local service that returns WAV audio for TTS and JSON transcripts for STT.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
