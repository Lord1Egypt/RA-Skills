## Description:

MiniMax Text-to-Speech synthesis using the HTTP REST API generates audio from text in 40+ languages with streaming and non-streaming modes, mp3, wav, and pcm formats, voice effects, and MiniMax TTS voice selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate narrated audio, voiceovers, and text-to-speech files through MiniMax REST APIs. It supports multilingual voice selection, streaming or non-streaming synthesis, and mp3, wav, or pcm output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends submitted text to MiniMax for synthesis.

Mitigation: Use it only with text that is appropriate to share with MiniMax and review data-handling requirements before routine use.

Risk: The skill allows overriding the API URL, which can expose the MiniMax API key and submitted text to an untrusted endpoint.

Mitigation: Use only trusted MiniMax endpoints; avoid passing --api_url in routine use or restrict the endpoint override before installation.

## Reference(s):

- [MiniMax TTS Voice Reference](references/voices.md)
- [MiniMax Voice Management API](https://platform.minimax.io/docs/api-reference/voice-management-get)
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/minimax-tts)
- [ClawHub publisher profile](https://clawhub.ai/user/fuzzyb33s)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with bash commands; scripts write audio files in mp3, wav, or pcm format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key and sends submitted text to the configured MiniMax-compatible endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
