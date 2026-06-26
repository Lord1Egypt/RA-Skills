## Description: <br>
Windows voice companion for OpenClaw with custom wake word activation, local speech-to-text, streamed gateway responses, ElevenLabs text-to-speech, multi-turn follow-up listening, mic suppression, and tray pause/resume controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurtivy](https://clawhub.ai/user/kurtivy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a Windows voice assistant that captures spoken prompts, sends recognized speech to an OpenClaw gateway, and plays spoken responses. It is intended for hands-free local interaction with an existing gateway setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microphone input and spoken interaction are privacy-sensitive. <br>
Mitigation: Install only when continuous voice interaction is expected, and pause or quit the tray app when listening should not be active. <br>
Risk: Recognized speech is sent to the configured OpenClaw gateway, and assistant response text is sent to ElevenLabs for text-to-speech. <br>
Mitigation: Keep GATEWAY_URL pointed at a trusted gateway and use the skill only with acceptable OpenClaw and ElevenLabs data handling expectations. <br>
Risk: Gateway, ElevenLabs, and Porcupine credentials are stored in local environment configuration. <br>
Mitigation: Protect the .env file and use a least-privileged gateway token. <br>


## Reference(s): <br>
- [Voice Assistant on ClawHub](https://clawhub.ai/kurtivy/openclaw-voice-assistant) <br>
- [Architecture](references/architecture.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Picovoice](https://picovoice.ai) <br>
- [Picovoice Console](https://console.picovoice.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and Python code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-focused assistant workflow requiring Python, microphone access, OpenClaw gateway credentials, ElevenLabs credentials, and a Porcupine access key.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
