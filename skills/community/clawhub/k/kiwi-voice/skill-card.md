## Description: <br>
Manage and configure Kiwi Voice assistant service. Use when starting/stopping Kiwi, editing voice config, checking logs, troubleshooting audio issues, or managing voice profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuangu260](https://clawhub.ai/user/yuangu260) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Kiwi Voice to run, configure, troubleshoot, and manage a self-hosted OpenClaw voice assistant with configurable STT, TTS, wake word, speaker profile, and approval settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is an always-listening voice assistant with broad voice-driven agent control and shipped configuration for provider, Home Assistant, Telegram, browser microphone, and speaker-profile workflows. <br>
Mitigation: Install only for that full assistant use case; change shipped tokens, bind or strongly protect the REST API, review integrations and microphone/profile storage, and narrow permissive prompts before exposing it to other speakers. <br>


## Reference(s): <br>
- [Kiwi Voice ClawHub release](https://clawhub.ai/yuangu260/kiwi-voice) <br>
- [Kiwi Voice documentation](https://docs.kiwi-voice.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [REST API](docs/api/rest.md) <br>
- [Voice Security](docs/features/voice-security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local service commands, configuration edits, log checks, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
