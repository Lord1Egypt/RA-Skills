## Description:

ElevenLabs advanced TTS for converting text to speech, listing voices, and managing credits

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to generate ElevenLabs text-to-speech audio, list and filter available voices, check credits, and integrate the bundled Python helper into workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose an ElevenLabs API key when passed directly on the command line.

Mitigation: Use ELEVENLABS_API_KEY from the environment or a secret manager instead of the --api-key option.

Risk: Text submitted for speech generation is sent to ElevenLabs for processing.

Mitigation: Do not submit sensitive or regulated text unless that external processing is acceptable for the intended use.

Risk: Generated audio can overwrite an existing file if the same output path is reused.

Mitigation: Choose a unique output filename or review the target path before generation.

## Reference(s):

- [Popular voices and API parameters](references/voices.md)
- [ElevenLabs API endpoint](https://api.elevenlabs.io/v1)
- [ClawHub skill page](https://clawhub.ai/mrnsmh/skills/openclaw-skill-elevenlabs-pro)
- [Publisher profile](https://clawhub.ai/user/mrnsmh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with bash and Python snippets; CLI output may be plain text, JSON, or generated MP3 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an ElevenLabs API key and can write audio output to a caller-selected path.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
