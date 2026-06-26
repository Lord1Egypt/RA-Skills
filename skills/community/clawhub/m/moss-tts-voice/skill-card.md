## Description: <br>
MOSS-TTS Voice helps agents generate MOSS Studio text-to-speech audio, clone voices from reference audio, and convert outputs for messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luogao2333](https://clawhub.ai/user/luogao2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate speech audio from text, clone authorized voices, and create channel-ready audio files for tools such as Feishu, Telegram, WhatsApp, Discord, Signal, and Slack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text and reference voice recordings are sent to MOSS Studio for speech generation or cloning. <br>
Mitigation: Use only non-sensitive text and recordings, and clone only voices the user has permission to use. <br>
Risk: The MOSS_API_KEY grants access to the external speech service. <br>
Mitigation: Keep the key in environment variables, avoid logs and repositories, and rotate it if exposure is suspected. <br>
Risk: Reference-audio and clone commands upload the file path provided by the user. <br>
Mitigation: Verify the exact audio file path before running clone or reference-audio commands. <br>


## Reference(s): <br>
- [MOSS Studio](https://studio.mosi.cn) <br>
- [MOSS-TTS API Technical Guide](references/api-guide.md) <br>
- [Channel Format Guide](references/channel-formats.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/luogao2333/moss-tts-voice) <br>
- [Publisher Profile](https://clawhub.ai/user/luogao2333) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, JSON status output, and generated audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audio files are written as WAV, OGG/Opus, or MP3 depending on the requested channel or format.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
