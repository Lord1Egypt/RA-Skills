## Description:

MiniMax TTS for FeiShu generates natural Chinese speech through MiniMax, supports voice selection, emotion detection, sound-effect tags, pause markers, and can send generated audio to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang92229](https://clawhub.ai/user/lixiang92229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to convert Chinese text or Feishu chat messages into speech, design or select MiniMax voices, and deliver generated audio to a Feishu recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chat-trigger flow can read and forward message content with weak scoping controls.

Mitigation: Install only in Feishu apps you control, restrict who can invoke trigger commands, and verify the recipient Open ID before use.

Risk: MiniMax and Feishu credentials enable paid API use and bot actions if exposed or over-permissioned.

Mitigation: Use minimal Feishu permissions, keep credentials in environment variables or a secret store, rotate them regularly, and avoid shared hosts for this version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixiang92229/skills/minimax-tts-feishu)
- [Project homepage](https://github.com/lixiang92229/lx-minimax-tts-feishu)
- [MiniMax Platform](https://platform.minimaxi.com)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, API calls]

**Output Format:** [Text status, Markdown voice catalog updates, WAV audio files, and Feishu audio messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MiniMax and Feishu credentials; generated audio may be sent to a configured Feishu Open ID.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
