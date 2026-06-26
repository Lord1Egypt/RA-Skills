## Description: <br>
Send native Feishu voice bubble messages via MiniMax TTS, converting text to 16kHz opus audio and delivering it as a playable Feishu audio bubble. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydoomed](https://clawhub.ai/user/raydoomed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to send generated voice replies as native Feishu audio bubbles instead of MP3 attachments. It is useful when a workflow needs text converted to speech with MiniMax and delivered to a Feishu recipient by open_id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-message text is sent to MiniMax for TTS processing. <br>
Mitigation: Do not use the skill for secrets, regulated data, or sensitive personal information unless MiniMax is approved for that use. <br>
Risk: Generated audio and recipient open_id are uploaded or sent through Feishu. <br>
Mitigation: Use only approved Feishu app permissions and recipients, and confirm the Feishu workspace policy allows this data flow. <br>
Risk: The skill depends on locally stored MiniMax and Feishu credentials. <br>
Mitigation: Store credentials only in the expected private config files, restrict file access, and rotate keys if they may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raydoomed/minimax-feishu-voice) <br>
- [MiniMax system voice IDs](https://platform.minimaxi.com/docs/faq/system-voice-id) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends generated audio through MiniMax TTS and Feishu APIs; requires ffmpeg with libopus support.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
