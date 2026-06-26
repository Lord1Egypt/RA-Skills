## Description: <br>
Converts text to MP3 speech with the MiniMax speech-2.8-hd API through an interactive token, text, and voice-selection workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggttol](https://clawhub.ai/user/ggttol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and messaging agents use this skill to collect a MiniMax API token, text content, and a voice choice, then generate an MP3 file for delivery through chat platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores one shared MiniMax API token locally in server/.env for the OpenClaw instance. <br>
Mitigation: Install only in trusted OpenClaw instances, remove server/.env when access should end, and rotate the MiniMax token if local persistence is no longer acceptable. <br>
Risk: Text submitted for conversion is sent to MiniMax for text-to-speech processing. <br>
Mitigation: Avoid converting private, regulated, or sensitive text unless MiniMax processing is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ggttol/minimax-tts-zh) <br>
- [MiniMax developer site](https://minimaxi.com) <br>
- [MiniMax text-to-audio API endpoint](https://api.minimaxi.com/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, CLI status text, FILE path output, and MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates MP3 files under /tmp/openclaw by default and emits a FILE: path for platform media delivery.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
