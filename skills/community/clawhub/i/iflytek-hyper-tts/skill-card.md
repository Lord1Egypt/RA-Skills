## Description:

Converts user-provided text into iFlytek Hyper TTS speech with selectable voices, speech rate, volume, pitch, sample rate, and MP3 output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to synthesize spoken audio from text through iFlytek's Hyper TTS service, including selecting supported voices and basic prosody settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to iFlytek's remote service.

Mitigation: Avoid submitting secrets, regulated data, or private content unless that use is approved.

Risk: The skill requires iFlytek API credentials in environment variables.

Mitigation: Store credentials in a secret manager or protected environment, keep them out of source files and prompts, and rotate them if exposed.

Risk: The documented dependency installation may pull the latest websocket-client package implicitly.

Mitigation: Install in a virtual environment and pin or lock websocket-client for reproducible deployments.

Risk: Generated audio is written to a local output path.

Mitigation: Choose intended workspace paths and review generated files before sharing or publishing them.

## Reference(s):

- [iFlytek Hyper TTS API documentation](https://www.xfyun.cn/doc/spark/super%20smart-tts.html)
- [iFlytek Hyper TTS voice list](https://www.xfyun.cn/doc/spark/super%20smart-tts.html#%E5%8F%91%E9%9F%B3%E4%BA%BA%E5%88%97%E8%A1%A8)
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/skills/iflytek-hyper-tts)
- [ClawHub publisher profile](https://clawhub.ai/user/iflytek.skills)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [JSON status output and local MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET environment variables; input text is limited to 64KB.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
