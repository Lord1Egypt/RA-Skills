## Description: <br>
Monitors YouTube and Bilibili live streams in a headed browser session and uses browser SpeechRecognition for real-time transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxu1232](https://clawhub.ai/user/xiaoxu1232) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to open supported live streams, check whether a stream appears live, and collect browser-generated speech transcripts for a selected listening duration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start microphone-based browser speech recognition during a headed browser session, and the privacy impact is under-documented. <br>
Mitigation: Use it only for streams and environments where microphone-based transcription is acceptable, and require publisher documentation for captured audio, transcription handling, storage, and sharing before broader deployment. <br>
Risk: The release advertises keyword alerts, but the security evidence says real keyword-alert logic is not implemented. <br>
Mitigation: Treat current output as transcription and stream-status monitoring until keyword matching and notification behavior are implemented and reviewed. <br>
Risk: Automatic media permission handling may obscure when browser audio or microphone access is active. <br>
Mitigation: Run in an isolated headed browser profile, review browser permission prompts and flags, and remove or justify automatic media permission handling before trusted use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoxu1232/live-stream-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoxu1232) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Console text and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcription depends on a headed browser, microphone permission, platform playback, and browser SpeechRecognition support.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
