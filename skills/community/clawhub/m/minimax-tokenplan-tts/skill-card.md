## Description:

Generate speech audio from text with MiniMax speech-2.8-hd, including selectable voices, speed, pitch, volume controls, WAV file output, and WebSocket streaming playback through ffplay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4833675](https://clawhub.ai/user/4833675)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert supplied text into MiniMax TTS audio, either as saved WAV/MP3 output or immediate streaming playback. It is suited for text-to-speech responses, narration, voice selection, and speech parameter tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed if a real MiniMax API key is pasted into SKILL.md or committed into the Python scripts.

Mitigation: Use an environment variable or secret store for MINIMAX_API_KEY, and review files before sharing or committing configured copies.

Risk: Streaming playback weakens TLS protections and can be unsafe on untrusted networks or endpoints.

Mitigation: Avoid streaming mode until TLS verification is fixed; use only trusted MiniMax base URLs and prefer non-streaming generation when secure transport cannot be confirmed.

Risk: Input text is transmitted to a third-party TTS service.

Mitigation: Do not send sensitive, confidential, or regulated text unless the MiniMax service terms and data handling are approved for that use.

## Reference(s):

- [MiniMax Speech T2A API Reference](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http)
- [MiniMax System Voice ID FAQ](https://platform.minimaxi.com/docs/faq/system-voice-id)
- [ClawHub Skill Page](https://clawhub.ai/4833675/skills/minimax-tokenplan-tts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts return file paths or streaming status on stdout and audio files on disk when saving is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [TTS input text is limited to 10000 characters; generated file mode writes WAV output by default, and streaming mode can play via ffplay or optionally save MP3 audio.]

## Skill Version(s):

1.0.1 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md released 2026-04-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
