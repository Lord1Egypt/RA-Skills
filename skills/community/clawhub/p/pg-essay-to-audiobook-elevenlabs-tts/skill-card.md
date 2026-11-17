## Description:

ElevenLabs Text-to-Speech API for high-quality speech synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call the ElevenLabs Text-to-Speech API, configure voices and model settings, and generate MP3 speech audio from text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech synthesis and the ElevenLabs API key are sent to ElevenLabs.

Mitigation: Use the skill only for text that is appropriate to share with ElevenLabs, protect the ELEVENLABS_API_KEY environment variable, and review ElevenLabs' data and billing terms before using private, regulated, or customer-provided text.

Risk: Generated audio is written to local MP3 files when the example code is executed.

Mitigation: Store generated files only in approved locations and apply the same handling controls used for the source text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/pg-essay-to-audiobook-elevenlabs-tts)
- [Publisher profile](https://clawhub.ai/user/lnj22)
- [ElevenLabs Text-to-Speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local MP3 audio files when the generated API-call code is executed with a valid ElevenLabs API key.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
