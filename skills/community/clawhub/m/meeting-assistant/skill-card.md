## Description: <br>
Build and troubleshoot SenseAudio meeting assistants for live transcription, speaker-aware meeting records, real-time translation, meeting notes, action items, and transcript export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams building meeting workflows use this skill to design and troubleshoot SenseAudio ASR integrations for live captions, recorded transcription, speaker-aware notes, translation, action items, and transcript export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting audio and transcripts can contain sensitive information and may be sent to or stored by SenseAudio. <br>
Mitigation: Use the skill only when SenseAudio is trusted for the meeting data, store the API key securely, confirm participant and organizational consent, and define retention and deletion handling for recordings, transcripts, logs, history, and archives. <br>
Risk: Generated meeting notes, decisions, and action items may be interpreted as authoritative even when ownership, deadlines, or conclusions are uncertain. <br>
Mitigation: Keep summaries tied to transcript segments, speakers, and timestamps; mark uncertain owners or due dates as unknown; and review meeting outputs before relying on them. <br>


## Reference(s): <br>
- [Realtime Workflow](references/realtime-workflow.md) <br>
- [Offline Meeting Transcription](references/offline-meeting-transcription.md) <br>
- [Note Generation](references/note-generation.md) <br>
- [Examples](references/examples.md) <br>
- [SenseAudio Homepage](https://nightly.senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown with code blocks, JSON examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, model selection guidance, transcript schemas, and meeting-note checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
