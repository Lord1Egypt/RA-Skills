## Description: <br>
MiniMax TTS Plus generates text-to-speech audio with selectable MiniMax voices and can produce local MP3 output or prepare/send voice messages for Telegram and Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vshen009](https://clawhub.ai/user/vshen009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add MiniMax text-to-speech output to agent workflows, including local audio generation and optional voice-message delivery through Telegram or Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech synthesis is sent to the MiniMax API. <br>
Mitigation: Do not synthesize sensitive text unless that use is approved, and protect the MINIMAX_API_KEY credential. <br>
Risk: When Telegram credentials are configured, generated audio and captions can be sent to the configured Telegram chat. <br>
Mitigation: Use --generate-only when local audio is sufficient, verify the target chat before sending, and protect TELEGRAM_BOT_TOKEN and TELEGRAM_TARGET. <br>
Risk: Generated audio files may persist in the workspace and can contain sensitive spoken content. <br>
Mitigation: Delete generated audio files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vshen009/minimax-tts-plus) <br>
- [MiniMax Speech T2A API documentation](https://platform.minimax.io/docs/api-reference/speech-t2a-http) <br>
- [MiniMax developer portal](https://platform.minimax.io) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, files] <br>
**Output Format:** [JSON status objects and generated audio files, with setup guidance in Markdown and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates MP3 audio locally by default, can transcode to OGG/Opus for Feishu, and can optionally send voice messages through Telegram when credentials are configured.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
