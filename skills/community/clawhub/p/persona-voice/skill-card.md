## Description:

Persona Voice helps an agent create short persona-styled replies for Feishu or Lark bots, optionally transcribe user audio with SenseAudio ASR, synthesize the reply with SenseAudio TTS, and send it as a native Feishu voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bot operators use this skill to add randomized or fixed persona voice replies to Feishu or Lark chat workflows. It supports text input and audio input, using SenseAudio for ASR/TTS and Feishu APIs for native voice-message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The transcription command can upload any readable local path supplied through --audio to SenseAudio.

Mitigation: Run the skill in a constrained runtime and only allow trusted server code to choose audio paths from an approved upload directory.

Risk: Voice content, generated text, audio files, and Feishu chat identifiers may leave the local environment for SenseAudio and Feishu processing.

Mitigation: Use the skill only where those providers are approved for the data involved, and avoid sending sensitive content without appropriate user notice and access controls.

Risk: Custom Feishu or SenseAudio base URLs could redirect credentials or content to an untrusted endpoint.

Mitigation: Keep the documented default service URLs unless the replacement endpoint is fully trusted and controlled.

Risk: Local .env files can contain Feishu and SenseAudio credentials.

Mitigation: Protect .env and .env.local files with local file permissions and exclude them from release artifacts and logs.

## Reference(s):

- [Feishu / Lark Integration Notes](references/feishu_integration.md)
- [Current Persona Presets](references/personas.md)
- [Provider Integration Notes](references/provider_notes.md)
- [Feishu Open Platform](https://open.feishu.cn)
- [SenseAudio API Endpoint](https://api.senseaudio.cn)
- [ClawHub Skill Page](https://clawhub.ai/hei-maom/skills/persona-voice)
- [Publisher Profile](https://clawhub.ai/user/hei-maom)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files, API calls]

**Output Format:** [Markdown guidance, shell commands, JSON command responses, generated audio files, and Feishu voice-message API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu and SenseAudio credentials; may read local audio input and create MP3/OPUS audio outputs.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
