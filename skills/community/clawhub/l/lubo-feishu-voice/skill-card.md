## Description: <br>
Sends Feishu voice messages by generating NoizAI TTS audio and preparing it for OpenClaw voice delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lubo1012](https://clawhub.ai/user/lubo1012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to reply with spoken audio in Feishu, using NoizAI text-to-speech to generate an opus voice file and OpenClaw message delivery to send it as a voice bubble. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to NoizAI and the generated audio is delivered through Feishu. <br>
Mitigation: Avoid using the skill for sensitive, regulated, or proprietary content unless NoizAI and Feishu are approved for that data. <br>
Risk: The skill depends on the separate noizai-tts skill and Feishu voice-message parameters being configured correctly. <br>
Mitigation: Review and trust the noizai-tts dependency first, then verify that Feishu messages use asVoice true and contentType audio/opus before relying on the workflow. <br>
Risk: NOIZ_API_KEY is a sensitive credential when provided for authenticated NoizAI behavior. <br>
Mitigation: Provide NOIZ_API_KEY only when authenticated NoizAI behavior is intentional, and manage it through approved secret-handling mechanisms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lubo1012/lubo-feishu-voice) <br>
- [Publisher Profile](https://clawhub.ai/user/lubo1012) <br>
- [NoizAI API Endpoint](https://noiz.ai/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples; the helper script prints a generated opus audio file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw, Feishu message delivery, Python 3.6+, and the noizai-tts skill; may use NOIZ_API_KEY when authenticated NoizAI behavior is intended.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
