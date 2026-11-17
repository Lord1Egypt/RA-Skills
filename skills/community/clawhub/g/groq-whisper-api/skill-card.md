## Description:

Transcribe audio via Groq Automatic Speech Recognition (ASR) Models (Whisper).

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxceem](https://clawhub.ai/user/maxceem)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe selected audio files through Groq's Whisper-compatible speech-to-text API, with options for model, language, prompt, and text or JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports an argument-handling flaw that can unintentionally upload other local files.

Mitigation: Use only trusted literal values for --prompt, --model, and --language until non-file form fields are handled literally, and review commands before automated use.

Risk: Selected audio files are sent to Groq's API for transcription.

Mitigation: Use only recordings approved for external API processing, especially when audio may contain confidential content.

## Reference(s):

- [Groq Speech-to-Text documentation](https://console.groq.com/docs/speech-to-text)
- [Groq audio transcriptions endpoint](https://api.groq.com/openai/v1/audio/transcriptions)
- [ClawHub skill page](https://clawhub.ai/maxceem/skills/groq-whisper-api)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions]

**Output Format:** [Plain text or JSON transcript files, with the output path printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and GROQ_API_KEY; defaults to whisper-large-v3-turbo and writes <input>.txt unless JSON output or --out is selected.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
