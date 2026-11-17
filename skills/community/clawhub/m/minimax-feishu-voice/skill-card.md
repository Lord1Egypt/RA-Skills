## Description:

Send native Feishu voice bubble messages via MiniMax TTS, converting text to 16kHz opus audio and delivering it as a playable Feishu audio bubble.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydoomed](https://clawhub.ai/user/raydoomed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace operators use this skill to let an agent turn text into MiniMax speech and send it as a native Feishu voice bubble to a Feishu open_id recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send externally generated voice messages through Feishu, so accidental or unauthorized sends may reach real recipients.

Mitigation: Require explicit user confirmation before running the send command and verify the recipient open_id and message text before execution.

Risk: Message text and generated audio are processed by MiniMax and Feishu services.

Mitigation: Avoid sending secrets, regulated data, or private content unless that third-party processing is acceptable for the deployment.

Risk: The skill depends on local credentials for MiniMax and Feishu.

Mitigation: Store API keys and app secrets outside shared logs or prompts and review configuration permissions before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raydoomed/skills/minimax-feishu-voice)
- [MiniMax system voice ID documentation](https://platform.minimaxi.com/docs/faq/system-voice-id)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [MiniMax API endpoint](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script returns a Feishu message_id after generating, converting, uploading, and sending the voice message.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
