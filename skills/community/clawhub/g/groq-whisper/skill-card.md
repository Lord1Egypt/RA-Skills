## Description: <br>
Transcribe audio files using Groq's Whisper API (whisper-large-v3). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[directorvector](https://clawhub.ai/user/directorvector) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, developers, and agents use this skill to transcribe local audio or voice-message files through Groq's Whisper API when a text transcript is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio recordings are sent to Groq for cloud transcription. <br>
Mitigation: Use the skill only when cloud processing is acceptable, and avoid confidential, regulated, or third-party recordings unless approved. <br>
Risk: A Groq API key is required and may be stored on disk. <br>
Mitigation: Store credentials with restrictive file permissions or provide the key through the GROQ_API_KEY environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/directorvector/groq-whisper) <br>
- [Publisher profile](https://clawhub.ai/user/directorvector) <br>
- [Groq audio transcriptions endpoint](https://api.groq.com/openai/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Plain text transcription emitted to stdout, with setup and usage guidance in Markdown and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an audio file path and optional language code; requires curl, jq, and a Groq API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
