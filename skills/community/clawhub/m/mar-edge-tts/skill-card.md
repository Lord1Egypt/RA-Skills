## Description: <br>
Text-to-speech conversion using SkillBoss API Hub TTS service for generating audio from text with voice, language, speed, pitch, and subtitle options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill to turn requested text into spoken audio for accessibility, multitasking, voice messages, presentations, or other audio-first workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Provide the key only in the expected environment variable, protect it as a secret, and rotate it if exposed. <br>
Risk: Text submitted for conversion is sent to an external TTS provider. <br>
Mitigation: Avoid converting secrets, credentials, private messages, or regulated data unless that external processing is acceptable for the use case. <br>
Risk: Generated audio files can contain sensitive spoken content. <br>
Mitigation: Clean up generated audio files when they are no longer needed, especially for temporary or shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-edge-tts) <br>
- [Publisher profile](https://clawhub.ai/user/marjoriebroad) <br>
- [node-edge-tts guide](references/node_edge_tts_guide.md) <br>
- [Voice testing](https://tts.travisvn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and MEDIA audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate MP3 audio files and optional JSON subtitle files; requires SKILLBOSS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
