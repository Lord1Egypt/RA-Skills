## Description:

Generates speech with Xiaomi MiMo V2.5 TTS models, including preset voices, voice design, voice cloning, natural-language style control, director mode, emotion, dialect, and singing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcchenx345](https://clawhub.ai/user/xcchenx345)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate spoken audio from text, select or design voices, clone permitted voice samples, and optionally send generated audio as Feishu voice messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis text and voice-cloning samples are sent to Xiaomi MiMo.

Mitigation: Avoid sensitive text and use voice cloning only for voices you have permission to use.

Risk: The optional Feishu sender transmits generated audio, app credentials, and recipient IDs to Feishu APIs.

Mitigation: Use appropriate Feishu app credentials, protect them as secrets, and confirm the recipient ID before sending audio messages.

Risk: Voice cloning can create audio that sounds like a sampled person.

Mitigation: Clone only with permission and review generated speech before sharing or sending it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xcchenx345/skills/mimo-v25-tts)
- [Xiaomi MiMo API base endpoint](https://api.xiaomimimo.com/v1)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files, API calls]

**Output Format:** [Markdown guidance with inline shell commands; scripts produce WAV audio files and optional Feishu API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIMO_API_KEY for synthesis; Feishu delivery additionally requires FEISHU_APP_ID, FEISHU_APP_SECRET, ffmpeg, curl, and a recipient ID.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
