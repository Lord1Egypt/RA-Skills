## Description:

Inworld TTS generates MP3 speech audio from text through the Inworld.ai text-to-speech API, with options for voice, speaking rate, temperature, model, and streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gugic](https://clawhub.ai/user/gugic)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to turn text, spoken responses, or narration into MP3 audio files through Inworld.ai. It is useful when an agent needs to prepare shell commands, configuration, or workflow guidance for text-to-speech generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to Inworld.ai and may include sensitive content if users provide it.

Mitigation: Avoid synthesizing secrets, private data, or confidential text unless the Inworld.ai account and data-handling terms are appropriate for that content.

Risk: The skill requires an Inworld API key for authenticated requests.

Mitigation: Use a narrowly scoped key and store it in a protected secret store or permission-restricted environment file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gugic/skills/inworld-tts)
- [Inworld Platform](https://platform.inworld.ai)
- [Inworld API Examples](https://github.com/inworld-ai/inworld-api-examples)
- [Inworld TTS Voice Endpoint](https://api.inworld.ai/tts/v1/voice)
- [Inworld TTS Streaming Endpoint](https://api.inworld.ai/tts/v1/voice:stream)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and MP3 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio depends on the provided text, selected voice, speaking rate, temperature, model, and streaming mode.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
