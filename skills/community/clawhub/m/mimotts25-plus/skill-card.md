## Description:

小米 MiMo TTS 2.5 Plus — 增强版语音合成。兼容官方接口，支持预置音色/声音设计/克隆/导演模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[limingjing6666](https://clawhub.ai/user/limingjing6666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate expressive MiMo TTS audio from text, including preset voices, voice design, voice cloning, and director-style emotional guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text prompts, style context, and voice-clone recordings may be sent to MiMo or another configured API endpoint.

Mitigation: Use only trusted HTTPS MiMo endpoints, avoid sensitive text, and upload only voice samples you own or are authorized to use.

Risk: Changing MIMO_API_BASE or using --base-url can send the API key and synthesis payloads to an arbitrary host.

Mitigation: Do not point the skill at untrusted hosts or http:// endpoints; rotate the API key if it may have been exposed.

Risk: Voice cloning can reproduce characteristics from uploaded audio samples.

Mitigation: Confirm consent and usage rights for each sample before using the voice-clone mode.

## Reference(s):

- [MiMo TTS 2.5 Official API Docs](artifact/references/official-api-docs.md)
- [Xiaomi MiMo Open Platform](https://platform.xiaomimimo.com/)
- [MiMo Public API Endpoint](https://api.xiaomimimo.com/v1)
- [MiMo China API Endpoint](https://token-plan-cn.xiaomimimo.com/v1)
- [ClawHub Skill Page](https://clawhub.ai/limingjing6666/skills/mimotts25-plus)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts can save mp3, wav, or ogg audio files such as output.mp3.]

## Skill Version(s):

1.3.1 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
