## Description: <br>
Transcribe and organize voice memos with automatic categorization and information extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn voice notes, audio memos, or spoken notes into structured text, summaries, action items, and searchable memo records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files may be sent to a third-party transcription service. <br>
Mitigation: Use the skill only when SenseAudio retention, security, and compliance terms are acceptable, and prefer an explicit confirmation step before upload. <br>
Risk: The transcribed text, extracted dates, tasks, contacts, categories, or summaries may be incomplete or incorrect. <br>
Mitigation: Review and edit extracted information before using it for planning, records, or downstream automation. <br>
Risk: The skill requires an external API key. <br>
Mitigation: Store SENSEAUDIO_API_KEY in the environment and avoid embedding it in prompts, code snippets, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/memo) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio ASR API](https://senseaudio.cn/docs/speech_recognition/http_api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and JSON or Markdown output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and may send audio files to SenseAudio for transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
