## Description:

Generates Chinese text-to-speech audio with the MiniMax TTS API, including system and cloned voices and command-line controls for model, voice, speed, output format, and output file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whille](https://clawhub.ai/user/whille)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to turn supplied text into audio files through MiniMax TTS, choose available voices, and configure speech model, speed, pause, format, and output path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis text is sent to MiniMax to generate audio, which can expose private documents, secrets, or sensitive personal data.

Mitigation: Use only text that is acceptable to share with MiniMax, and avoid passing secrets, private documents, or sensitive personal data as TTS input.

Risk: The MiniMax API key must be available to the script through MINIMAX_API_KEY.

Mitigation: Install and run the skill only in environments where exposing MINIMAX_API_KEY to this script is acceptable.

## Reference(s):

- [MiniMax speech T2A HTTP API documentation](https://platform.minimax.io/docs/api-reference/speech-t2a-http)
- [MiniMax platform](https://platform.minimax.io)
- [ClawHub skill page](https://clawhub.ai/whille/skills/minimax-tts-cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated audio is written as an audio file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and sends synthesis text to the MiniMax API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
