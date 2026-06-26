## Description: <br>
Generates speech with Xiaomi MiMo V2.5 TTS models, including preset voices, voice design, voice cloning, natural-language style control, director mode, emotion and dialect tags, and singing support for preset voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcchenx345](https://clawhub.ai/user/xcchenx345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to synthesize Chinese or English speech, create or clone voice styles, save WAV audio files, and optionally send generated audio through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, style prompts, and voice samples may be sent to Xiaomi's MiMo API. <br>
Mitigation: Use the skill only when external MiMo API processing is acceptable for the content being synthesized. <br>
Risk: Voice cloning can reproduce a person's voice from an audio sample. <br>
Mitigation: Use voice cloning only with permission from the voice owner. <br>
Risk: Feishu message sending uses sensitive app credentials and can upload or send audio to an unintended recipient. <br>
Mitigation: Keep Feishu credentials least-privileged and require clear recipient confirmation before upload or send actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xcchenx345/mimo-v25-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce WAV audio files or Feishu audio-message API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIMO_API_KEY for MiMo API calls; Feishu sending also requires FEISHU_APP_ID and FEISHU_APP_SECRET.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
