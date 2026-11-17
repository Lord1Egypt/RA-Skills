## Description:

调用 MiniMax 语音合成 API 生成语音,发送语音消息。支持系统音色、克隆音色、流式/非流式输出。使用场景：用户需要生成高质量中文语音、语音合成、文本转语音。

This skill is ready for commercial/non-commercial use.

## Publisher:

[seacozz2007](https://clawhub.ai/user/seacozz2007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate Chinese text-to-speech audio with MiniMax voices, list available voices, and send generated audio through supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an embedded MiniMax API credential.

Mitigation: Remove the embedded key, rotate the exposed credential, and require each user to supply credentials through a protected secret source before use.

Risk: Text and generated audio may be sent to MiniMax or messaging platforms.

Mitigation: Clearly warn users before sending content externally and require explicit user control over destination channels, targets, and media paths.

## Reference(s):

- [MiniMax Speech T2A HTTP API documentation](https://platform.minimax.io/docs/api-reference/speech-t2a-http)
- [ClawHub skill page](https://clawhub.ai/seacozz2007/skills/minimax-tts-send)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with inline bash commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP3 audio files and outbound messaging commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
