## Description:

Transcribe audio files via Groq's OpenAI-compatible speech-to-text API. Use when the user sends voice messages or audio files and you need fast cloud speech-to-text through Groq instead of local Whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timing-up](https://clawhub.ai/user/timing-up)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to transcribe short voice notes or audio clips through Groq's cloud speech-to-text API, especially when they want a fast transcript for follow-up summarization or chat replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe prompt, model, or language values can cause curl to treat a value as a file upload and send unintended local files to Groq.

Mitigation: Use only trusted flag values, avoid values that begin with @, validate inputs before use, and prefer updating the script to use --form-string for non-file fields.

Risk: Groq API keys are required for use and may be exposed if stored or shared insecurely.

Mitigation: Store the key through the safest available credential mechanism and rotate it if it may have been exposed.

Risk: Audio files are sent to Groq's cloud transcription service.

Mitigation: Use only audio that is appropriate to process through Groq under the user's data-handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/timing-up/skills/groq-voice-transcribe)
- [Groq Console](https://console.groq.com/)
- [Groq OpenAI-Compatible Audio Transcriptions Endpoint](https://api.groq.com/openai/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [Plain text transcript or verbose JSON written to an output file; setup guidance is Markdown with shell and JSON snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Groq API key and sends selected audio files to Groq for transcription.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
