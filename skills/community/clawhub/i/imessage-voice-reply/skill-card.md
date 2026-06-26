## Description: <br>
Generates local Kokoro-ONNX text-to-speech audio for iMessage voice replies and prepares BlueBubbles send parameters for native inline voice bubbles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bolander72](https://clawhub.ai/user/bolander72) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to reply to iMessage voice messages with locally generated spoken responses through BlueBubbles. It is intended for cases where a voice response is explicitly requested or matches the sender's voice-message format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated voice replies can be sent to the wrong recipient or contain unintended content. <br>
Mitigation: Review the recipient, generated audio content, and BlueBubbles send payload before sending. <br>
Risk: Setup downloads unpinned Python packages and Kokoro model files. <br>
Mitigation: Install in an isolated environment and review package/model sources before use in sensitive environments. <br>
Risk: Native iMessage voice bubbles depend on macOS afconvert and BlueBubbles configuration. <br>
Mitigation: Confirm BlueBubbles is configured and test the expected CAF/Opus output path before relying on the skill for routine replies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bolander72/imessage-voice-reply) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON message payloads; generated runtime output is an audio file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CAF/Opus audio on macOS or MP3 via ffmpeg fallback; requires BlueBubbles for sending.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
