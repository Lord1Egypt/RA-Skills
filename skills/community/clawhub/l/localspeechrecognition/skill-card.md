## Description: <br>
Local Speech Recognition transcribes supported audio files into text locally with faster-whisper, supporting Chinese, English, Japanese, and automatic language detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zktufo](https://clawhub.ai/user/zktufo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert local voice messages, meeting audio, podcast audio, and other supported audio files into readable text without sending audio to a third-party transcription API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text transcribed from third-party audio may be injected into the conversation automatically and could be mistaken for user instructions. <br>
Mitigation: Treat transcribed audio as untrusted content unless the speaker and context are trusted; review the text before acting on it. <br>
Risk: First use may fetch a Whisper model or dependency for local transcription. <br>
Mitigation: Install only in environments where local model or dependency downloads are allowed, and review dependency sources before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zktufo/localspeechrecognition) <br>
- [Publisher profile](https://clawhub.ai/user/zktufo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcription output with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports .ogg, .m4a, .mp3, and .wav audio files up to 25MB; language can be set to zh, en, ja, or auto.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
