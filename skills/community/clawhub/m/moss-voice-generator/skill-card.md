## Description:

MOSI Studio 指令式音色生成 skill that helps an agent generate speech by sending text and a natural-language voice-style description to MOSI Studio, then saving the returned audio as a WAV file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkkb473](https://clawhub.ai/user/mkkb473)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to create one-off or exploratory voice audio from written text without choosing a preset voice_id. It is suited for generating described voice styles and preparing WAV output for downstream delivery, including Feishu voice-bubble workflows when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text to be spoken and the voice-style description are sent to MOSI Studio for processing.

Mitigation: Avoid sensitive text or confidential voice-style descriptions unless MOSI Studio processing is approved for that data.

Risk: Supplying the API key with --api-key can expose the credential through shell history or process listings.

Mitigation: Set MOSI_TTS_API_KEY through the environment or a secret manager instead of passing the key on the command line.

Risk: Generated audio may be forwarded into Feishu chats.

Mitigation: Confirm the destination and intended recipients before sending generated audio into Feishu.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mkkb473/skills/moss-voice-generator)
- [MOSI Studio](https://studio.mosi.cn)
- [MOSI Studio Speech API](https://studio.mosi.cn/api/v1/audio/speech)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; the script writes a WAV audio file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOSI_TTS_API_KEY plus curl, jq, and base64. Default output is a 24 kHz WAV file at ~/.openclaw/workspace/voice_gen_output.wav unless an output path is supplied.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
