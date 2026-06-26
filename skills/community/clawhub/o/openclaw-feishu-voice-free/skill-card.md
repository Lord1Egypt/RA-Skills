## Description: <br>
Adds local Feishu voice chat support for OpenClaw by using Whisper for speech recognition and Qwen3-TTS for speech synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuaishi1991](https://clawhub.ai/user/shuaishi1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to handle Feishu voice messages locally, transcribe incoming audio, generate assistant replies, and return synthesized voice responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled configuration may contain sensitive credentials or tokens. <br>
Mitigation: Replace the bundled openclaw.json with a minimal local configuration and rotate any exposed secrets before use. <br>
Risk: Voice-processing services may be reachable beyond the local machine if exposed on a broad network interface. <br>
Mitigation: Bind services to 127.0.0.1 where possible, use firewall controls, and avoid running the services as root. <br>
Risk: Voice cloning can process biometric voice data and may be misused without consent. <br>
Mitigation: Clone voices only with explicit permission and keep generated voice embeddings protected. <br>
Risk: Remote clone mode can send voice data to another endpoint. <br>
Mitigation: Use remote clone mode only with a trusted endpoint and an accepted data-handling policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuaishi1991/openclaw-feishu-voice-free) <br>
- [Publisher profile](https://clawhub.ai/user/shuaishi1991) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) <br>
- [Whisper](https://github.com/openai/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Audio, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and local HTTP service responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local text transcription and synthesized audio when the required models and services are running.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
