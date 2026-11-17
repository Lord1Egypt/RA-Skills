## Description:

MiniMax TTS Plus lets an agent turn text into speech with MiniMax voices, generate MP3 audio, optionally transcode Feishu voice messages to OGG/Opus, and send Telegram voice messages when configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vshen009](https://clawhub.ai/user/vshen009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add text-to-speech output to OpenClaw workflows, including generated audio files and optional delivery to Telegram or Feishu. It is useful when an agent needs spoken responses, per-agent voice selection, or channel-native voice message formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TTS text is sent to the MiniMax API service.

Mitigation: Avoid sending sensitive or regulated content unless the deployment owner has approved MiniMax API use for that data.

Risk: Default wrapper mode can send generated audio to a configured Telegram chat.

Mitigation: Use --generate-only when message delivery is not intended and verify TELEGRAM_TARGET before enabling Telegram sending.

Risk: The security review reports unsafe handling of Telegram bot credentials in the delivery path.

Mitigation: Keep .env private, use a low-privilege Telegram bot, and address the reported curl token exposure and .env allowlist concerns before production use.

## Reference(s):

- [MiniMax Speech T2A HTTP API Documentation](https://platform.minimax.io/docs/api-reference/speech-t2a-http)
- [MiniMax Developer Platform](https://platform.minimax.io)
- [MiniMax API Endpoint](https://api.minimaxi.com)
- [ClawHub Skill Page](https://clawhub.ai/vshen009/skills/minimax-tts-plus)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files, guidance]

**Output Format:** [JSON status objects, generated audio files, and Markdown usage examples with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates MP3 audio by default, can produce OGG/Opus for Feishu, and can send Telegram voice messages when Telegram credentials and a target are configured.]

## Skill Version(s):

1.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
