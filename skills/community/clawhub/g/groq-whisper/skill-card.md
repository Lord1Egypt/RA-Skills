## Description:

Transcribes audio files using Groq's Whisper API with the whisper-large-v3 model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[directorvector](https://clawhub.ai/user/directorvector)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to transcribe user-provided voice messages or audio files through Groq's cloud Whisper API when cloud transcription is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files may be uploaded to Groq's cloud API without clear user confirmation.

Mitigation: Invoke the skill only after an explicit user request or approval, and avoid sending sensitive recordings unless the user has approved cloud processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/directorvector/skills/groq-whisper)
- [Skill source manifest](artifact/SKILL.md)
- [Transcription script](artifact/scripts/transcribe.sh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription output with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a Groq API key provided by GROQ_API_KEY or ~/.config/groq/credentials.json.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
