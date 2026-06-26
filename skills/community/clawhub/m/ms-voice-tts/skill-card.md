## Description: <br>
Generates high-quality Chinese text-to-speech voice messages with edge-tts and prepares them for delivery through messaging channels such as Feishu, Telegram, and Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binbin1213](https://clawhub.ai/user/binbin1213) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn short Chinese text into local audio files and send them as voice messages in supported chat channels. It is useful for spoken notifications, replies, announcements, and customer-support style messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent to edge-tts may be processed by a third-party text-to-speech service. <br>
Mitigation: Avoid converting secrets, credentials, or confidential text. <br>
Risk: Generated audio files are retained locally until removed. <br>
Mitigation: Delete generated audio files when they are no longer needed. <br>
Risk: Voice files can be sent to the wrong messaging channel. <br>
Mitigation: Confirm the destination channel before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/binbin1213/ms-voice-tts) <br>
- [Publisher Profile](https://clawhub.ai/user/binbin1213) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON message examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local opus audio file paths for downstream message sending; generated audio should be deleted when no longer needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
