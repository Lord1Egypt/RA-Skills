## Description: <br>
Transcribe audio files via Groq's OpenAI-compatible speech-to-text API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Timing-up](https://clawhub.ai/user/Timing-up) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe voice notes and short audio clips through Groq for follow-up summarization, chat replies, or plain transcript generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to Groq for cloud transcription, which may expose private or sensitive speech content to an external service. <br>
Mitigation: Use this skill only for recordings that are acceptable to process with Groq, and review Groq's privacy and retention terms for the intended use case. <br>
Risk: The skill requires a Groq API key for transcription requests. <br>
Mitigation: Use a dedicated, revocable Groq API key and avoid transcribing recordings that contain secrets or sensitive conversations unless that processing is acceptable. <br>


## Reference(s): <br>
- [Groq Console](https://console.groq.com/) <br>
- [Groq OpenAI-compatible transcription endpoint](https://api.groq.com/openai/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Plain text transcript or verbose JSON file, with shell command examples and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default model is whisper-large-v3-turbo; output defaults to a .txt file beside the input audio, or .json when verbose JSON is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
