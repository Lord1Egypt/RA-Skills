## Description:

Text-to-speech (TTS) via ElevenLabs for voice replies, spoken versions of text, or requests for voice notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate MP3 speech from supplied text with ElevenLabs, typically when a conversation should return an audio or voice-note artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can overwrite any output path that the running account can write.

Mitigation: Constrain outputs to a safe workspace directory, use unique filenames, and refuse overwrites before broad deployment.

Risk: Text provided for speech generation is sent to ElevenLabs.

Mitigation: Avoid generating speech from sensitive text unless the user accepts that external processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-tts)
- [Publisher profile](https://clawhub.ai/user/elandivar)
- [ElevenLabs Text-to-Speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and an audio file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an MP3 audio file by default; requires ELEVENLABS_API_KEY and either ELEVENLABS_VOICE_ID or an explicit voice id.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
