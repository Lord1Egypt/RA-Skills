## Description: <br>
Helps users remember where they put things and schedule voice reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q1lin570](https://clawhub.ai/user/q1lin570) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and assistants use this skill to record item locations, retrieve them later, and schedule spoken reminders for personal tasks or appointments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Item locations and reminders are stored in local JSON files. <br>
Mitigation: Avoid recording secrets or highly sensitive locations, and protect the local data directory with normal device and filesystem controls. <br>
Risk: Text selected for speech is sent to SenseAudio for TTS generation. <br>
Mitigation: Review spoken reminder text before use and do not send confidential content unless the deployment's SenseAudio terms and data-handling requirements are acceptable. <br>
Risk: Daemon or scheduled-task mode can run ongoing background reminder checks. <br>
Mitigation: Enable daemon or scheduled execution only when persistent reminders are intended, and review the configured interval and local reminder list. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q1lin570/memory-assistant) <br>
- [SenseAudio documentation](https://senseaudio.cn/docs) <br>
- [SenseAudio text-to-speech API](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio voice API](https://senseaudio.cn/docs/voice_api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or play audio through SenseAudio TTS when configured with SENSEAUDIO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
