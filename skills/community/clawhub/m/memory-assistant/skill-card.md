## Description:

Memory Assistant helps users record item locations and schedule time-based voice reminders, including SenseAudio TTS alerts for saved locations and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q1lin570](https://clawhub.ai/user/q1lin570)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record item locations, query those locations later, and schedule voice reminders for personal tasks. The skill can also guide an agent to generate or run helper commands that synthesize reminder and location text through SenseAudio TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal reminder and item-location text may be stored locally.

Mitigation: Review the configured storage path before use and avoid recording highly sensitive locations, secrets, or regulated personal information.

Risk: Reminder and location text may be sent to SenseAudio for text-to-speech generation.

Mitigation: Use the skill only when cloud TTS exposure is acceptable, and avoid sending sensitive travel, medical, financial, or secret information.

Risk: The helper scripts can write local JSON state and generated audio files, and the reminder runner can be used as a daemon or scheduled task.

Mitigation: Review file-writing behavior and scheduled execution settings before enabling the daemon or cron/task scheduler integration.

## Reference(s):

- [Reference](reference.md)
- [Examples](examples.md)
- [SenseAudio Documentation](https://senseaudio.cn/docs)
- [SenseAudio Text-to-Speech API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio Voice API](https://senseaudio.cn/docs/voice_api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON data examples, Python helper scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local reminder and item-location JSON files and generate audio files through SenseAudio TTS helper scripts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
