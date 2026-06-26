## Description: <br>
Control JoyIn AI robots (W-1 Walle / M-1 Mini) for movement, follow behavior, media, live stream, TTS, agent configuration, and device status via OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanfang724](https://clawhub.ai/user/yanfang724) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robot operators use this skill through OpenClaw to check device readiness and operate JoyIn W-1/M-1 robots. It supports movement, status checks, live video, TTS, WiFi setup, LLM registration, and agent binding tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad robot-control authority can cause physical movement or interrupt active robot modes. <br>
Mitigation: Run preflight before robot commands, supervise physical movement, and avoid interrupting OTA, mapping, charging, patrol, guard, or follow modes unless intentionally stopping or changing state. <br>
Risk: Camera/audio data, stream URLs, ASR output, JoyIn auth keys, WiFi passwords, and LLM API keys are sensitive. <br>
Mitigation: Limit use to trusted operators, prefer environment-backed credentials, and avoid sharing command output that contains stream URLs, transcripts, or secrets. <br>
Risk: WiFi, LLM registration, and agent-binding commands can make lasting robot or service configuration changes. <br>
Mitigation: Use these commands only after confirming the target device, API endpoint, and requested change with the operator. <br>


## Reference(s): <br>
- [JoyIn Robot Control on ClawHub](https://clawhub.ai/yanfang724/joyin-robot-control) <br>
- [yanfang724 ClawHub Publisher Profile](https://clawhub.ai/user/yanfang724) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JOYIN_API_BASE, JOYIN_AUTH_KEY, and JOYIN_DEVICE_SN.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
