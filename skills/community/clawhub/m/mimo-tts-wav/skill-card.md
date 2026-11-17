## Description:

Generates Chinese and English speech with Xiaomi MiMo V2.5 TTS using preset voices, text-described voice design, or consent-based voice cloning, with optional Feishu voice-message delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcchenx345](https://clawhub.ai/user/xcchenx345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn text into speech, design voices from text descriptions, clone voices from user-provided audio samples, and optionally deliver generated audio as Feishu voice messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TTS text, style context, and voice-cloning samples are sent to Xiaomi MiMo.

Mitigation: Avoid sensitive content unless the user accepts that remote-service exposure, keep MiMo API keys scoped, and use voice cloning only with consent from the voice owner.

Risk: Optional Feishu delivery sends generated audio and recipient identifiers to Feishu.

Mitigation: Use Feishu delivery only for intended recipients and avoid untrusted receiver values until the sending script validates and JSON-encodes them safely.

## Reference(s):

- [ClawHub skill release: mimo-tts-wav](https://clawhub.ai/xcchenx345/skills/mimo-tts-wav)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with command examples; scripts produce WAV audio files and optional Feishu audio messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIMO_API_KEY for MiMo TTS. Optional Feishu delivery requires FEISHU_APP_ID, FEISHU_APP_SECRET, ffmpeg, curl, and recipient identifiers.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
