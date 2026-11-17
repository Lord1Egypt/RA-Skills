## Description:

MiniMax Text-to-Speech synthesis using the HTTP REST API for creating spoken audio from text with multilingual voices, streaming or non-streaming generation, common audio formats, and voice effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert text into voiceovers, narrated content, and other spoken audio through MiniMax TTS. It is useful when an agent needs to select voices, configure speech parameters, and run the included CLI script to produce audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the MiniMax bearer token and text to a caller-supplied API URL.

Mitigation: Use only non-sensitive text, keep MINIMAX_API_KEY scoped and rotatable, and restrict --api_url to approved MiniMax HTTPS endpoints.

## Reference(s):

- [MiniMax TTS Voice Reference](artifact/references/voices.md)
- [MiniMax TTS API endpoint](https://api.minimax.io/v1/t2a_v2)
- [MiniMax TTS lower-latency API endpoint](https://api-uw.minimax.io/v1/t2a_v2)
- [MiniMax Voice Management API](https://platform.minimax.io/docs/api-reference/voice-management-get)
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/minimax-tts-pro)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with CLI commands; generated audio files in mp3, wav, or pcm format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MiniMax API credentials and may write audio output to a user-specified file path.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
