## Description: <br>
Transcribe audio via Groq Automatic Speech Recognition (ASR) Models (Whisper). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxceem](https://clawhub.ai/user/maxceem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to transcribe selected local audio files through Groq's Whisper-compatible speech-to-text API and save plain text or JSON transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to Groq for transcription. <br>
Mitigation: Avoid confidential or regulated recordings unless organizational policy permits Groq processing. <br>
Risk: The skill requires a Groq API key. <br>
Mitigation: Keep GROQ_API_KEY out of shared files, commits, and backups. <br>


## Reference(s): <br>
- [Groq speech-to-text documentation](https://console.groq.com/docs/speech-to-text) <br>
- [ClawHub skill page](https://clawhub.ai/maxceem/groq-whisper-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text transcript or JSON transcription file, with shell command usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and GROQ_API_KEY; supports model, language, prompt, output path, and JSON response options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
