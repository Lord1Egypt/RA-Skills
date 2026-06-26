## Description: <br>
Convert text to speech with the MiniMax TTS API and prepare Feishu-compatible voice bubble replies when a user requests a voice response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronjager92](https://clawhub.ai/user/aaronjager92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu bot operators use this skill to turn requested text replies into OGG/Opus voice messages generated through MiniMax TTS. It is intended for explicit voice-reply triggers such as /voice or Chinese voice reply commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-reply text is sent to MiniMax and the generated audio is shared through Feishu, which can expose sensitive content. <br>
Mitigation: Use explicit triggers, avoid sensitive or regulated content, and confirm users are comfortable with MiniMax and Feishu processing the content. <br>
Risk: A local config.txt file can expose the MiniMax API key if it is mishandled. <br>
Mitigation: Prefer the MINIMAX_VOICE_API_KEY environment variable and protect any local config.txt file. <br>


## Reference(s): <br>
- [Skill README](artifact/references/README.md) <br>
- [MiniMax Open Platform](https://www.minimaxi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated OGG audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key, network access to MiniMax, the Python requests package, and ffmpeg for MP3 to OGG/Opus conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
