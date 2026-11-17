## Description:

Generate voice audio and transcribe speech using MiniMax TTS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate English or Spanish speech audio through MiniMax TTS and to transcribe supplied audio files with local Whisper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text sent for speech generation is submitted to MiniMax using the configured API key and may contain sensitive information.

Mitigation: Do not use the skill with secrets or highly sensitive text, and review MiniMax data handling requirements before use.

Risk: Generated audio and transcript files are saved in a predictable workspace path by default.

Mitigation: Set KAI_MINIMAX_WORKSPACE to an access-controlled location and manage generated files according to local retention and privacy policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ogdegenblaze/skills/kai-minimax-tts)
- [MiniMax TTS API endpoint used by the skill](https://api-uw.minimax.io/v1/t2a_v2)
- [Publisher profile](https://clawhub.ai/user/ogdegenblaze)

## Skill Output:

**Output Type(s):** [audio, text, shell commands, configuration]

**Output Format:** [MP3 audio file, plain-text transcript file, and Markdown setup or usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated voice is saved as Kai.mp3, and transcription output is saved as latest_from_blaze.txt in the configured workspace.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
