## Description: <br>
Send voice messages on Lark (Feishu) by converting text to speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheerwhy](https://clawhub.ai/user/cheerwhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to generate speech from text, convert it to Feishu-compatible Opus audio, and send it as a Lark voice message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A voice message could be sent to the wrong recipient or contain unintended spoken content. <br>
Mitigation: Confirm the recipient and spoken text before sending the message. <br>
Risk: Generated speech may include sensitive text, and temporary audio files are stored under /tmp/openclaw/. <br>
Mitigation: Use a trusted TTS source and avoid highly sensitive content unless temporary local audio storage is acceptable. <br>
Risk: Voice delivery depends on ffmpeg conversion to the Opus format expected by Feishu. <br>
Mitigation: Verify ffmpeg is installed and confirm the converted audio before sending when message accuracy matters. <br>


## Reference(s): <br>
- [ClawHub release: Lark (Feishu) Voice](https://clawhub.ai/cheerwhy/lark-voice) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Tool calls, Audio files] <br>
**Output Format:** [Markdown instructions with bash and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and a TTS source; generated audio is temporarily stored under /tmp/openclaw/.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
