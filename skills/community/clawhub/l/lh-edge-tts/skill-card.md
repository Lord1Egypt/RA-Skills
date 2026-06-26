## Description: <br>
Converts text to speech with Python edge-tts, supporting multiple voices, languages, speed, pitch, volume, and subtitle output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhedev](https://clawhub.ai/user/liuhedev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to turn requested text or text files into spoken MP3 audio, optionally choosing voice, language, speed, pitch, volume, and subtitle output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text converted by the skill is processed by an online Microsoft Edge TTS service. <br>
Mitigation: Do not convert secrets, credentials, private documents, or regulated data unless the use is approved. <br>
Risk: Unexpected voice, proxy, or output behavior can result from saved local TTS preferences. <br>
Mitigation: Review ~/.tts-config.json and use explicit input and output paths when behavior matters. <br>


## Reference(s): <br>
- [LH Edge TTS ClawHub release](https://clawhub.ai/liuhedev/lh-edge-tts) <br>
- [Voice testing resource](https://tts.travisvn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration values, and generated audio or subtitle file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MP3 audio by default and can write VTT or SRT subtitles; uses an online Microsoft Edge TTS service and may store preferences in ~/.tts-config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill-info.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
