## Description: <br>
Local macOS voice-control integration for OpenClaw. Use when setting up, deploying, troubleshooting, or operating wakeword-triggered voice access to a local OpenClaw agent with ASR, TTS, overlay UI, and launchd background support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carrotyuan](https://clawhub.ai/user/carrotyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, validate, and maintain a local macOS voice-control entrypoint for an OpenClaw agent. It helps set up wakeword activation, local ASR, TTS playback, overlay UI, environment configuration, and optional launchd background service behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The voice entrypoint is not identity-bound, so anyone near the microphone may be able to trigger capabilities exposed by the connected OpenClaw agent. <br>
Mitigation: Use a limited-permission voice-facing agent, add explicit safety constraints, and require confirmation for high-risk actions. <br>
Risk: The skill uses sensitive local microphone access and an OpenClaw token. <br>
Mitigation: Keep the OpenClaw token private, avoid printing secrets, and store machine-specific secrets in the local environment file. <br>
Risk: Optional launchd background service behavior can create an always-available wakeword listener. <br>
Mitigation: Enable launchd auto-start only when persistent voice access is intended, and stop foreground validation before enabling background resident behavior. <br>
Risk: Repository setup and model downloads can change the local system or pull unreviewed code and assets. <br>
Mitigation: Review or pin the repository code before setup, confirm before fetching, installing, downloading models, or enabling background services. <br>


## Reference(s): <br>
- [OpenClaw Voice Control repository](https://github.com/CarrotYuan/openclaw-voice-control) <br>
- [OpenClaw Voice Control on ClawHub](https://clawhub.ai/carrotyuan/openclaw-voice-control) <br>
- [Picovoice](https://picovoice.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, validation, troubleshooting, maintenance, and safety guidance for a macOS-only local voice-control deployment.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
