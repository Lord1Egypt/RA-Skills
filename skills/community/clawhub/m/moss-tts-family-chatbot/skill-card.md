## Description:

MOSI Studio audio skill for ASR, text-to-speech, instructed voice generation, multi-speaker dialogue synthesis, voice cloning, sound-effect generation scaffolding, and Feishu voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkkb473](https://clawhub.ai/user/mkkb473)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to transcribe inbound audio, synthesize voice responses, generate multi-speaker audio, manage custom cloned voices, and send Feishu voice messages through MOSI Studio APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private audio or transcribed text may be uploaded to MOSI Studio or Feishu.

Mitigation: Install only in workspaces where users understand that audio and text can be sent to those services, and avoid processing private voice messages without authorization.

Risk: Voice cloning can imitate a speaker without adequate consent.

Mitigation: Use voice cloning only with explicit authorization from the speaker, and do not clone third parties, celebrities, coworkers, or customers without consent.

Risk: Feishu voice messages can be sent using available Feishu credentials.

Mitigation: Limit Feishu credential availability to trusted workspaces and require operator review before sending audio to chats.

Risk: The sound-effect feature is scaffolded while the artifact says the MOSI sound-effect REST interface was not publicly available as of 2026-03.

Mitigation: Treat sound-effect generation as unavailable until the MOSI API documentation confirms a supported endpoint.

## Reference(s):

- [MOSI API Reference](references/api.md)
- [MOSI Studio](https://studio.mosi.cn)
- [Skill page](https://clawhub.ai/mkkb473/skills/moss-tts-family-chatbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python commands, API request examples, and generated audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WAV or OPUS audio files, plain-text transcriptions, JSON API responses, and Feishu audio messages.]

## Skill Version(s):

0.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
