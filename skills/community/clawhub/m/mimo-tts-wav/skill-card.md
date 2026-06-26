## Description: <br>
MiMo V2.5 TTS generates speech with Xiaomi MiMo V2.5 models, including preset voices, voice design, voice cloning, natural-language style control, director mode, emotion and dialect tags, and singing for preset voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcchenx345](https://clawhub.ai/user/xcchenx345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate WAV speech from text with Xiaomi MiMo, choose preset or designed voices, clone authorized voice samples, and optionally send generated audio through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends TTS text, style prompts, and voice-cloning samples to Xiaomi MiMo. <br>
Mitigation: Use the skill only with text and voice samples that are appropriate to share with Xiaomi MiMo, and avoid sensitive or unauthorized voice data. <br>
Risk: Voice cloning can reproduce a person's voice without adequate consent. <br>
Mitigation: Use voice cloning only for voices the user is authorized to reproduce, and keep consent requirements explicit before running the voice-clone script. <br>
Risk: The Feishu helper can send generated audio to a private or group recipient. <br>
Mitigation: Confirm the Feishu recipient ID and recipient type before sending audio, and protect Feishu application credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xcchenx345/mimo-tts-wav) <br>
- [Publisher profile](https://clawhub.ai/user/xcchenx345) <br>
- [Xiaomi MiMo API endpoint](https://api.xiaomimimo.com/v1) <br>
- [Feishu Open Platform authentication endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python script usage that produces WAV audio files and optional Feishu audio messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MiMo credentials for TTS generation; Feishu credentials are required only when sending generated audio messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
