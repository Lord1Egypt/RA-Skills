## Description:

Meeting Recorder Assistant records and transcribes meeting audio, then generates minutes, action items, summaries, and sentiment-oriented meeting insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to record or transcribe meetings, generate structured minutes, and extract follow-up tasks from meeting transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting audio or transcripts may contain confidential, regulated, or personal information and can be sent to Google's speech-recognition service.

Mitigation: Use the skill only where recording is allowed, participants have provided required consent, and external transcription is acceptable; use a local transcription option for sensitive meetings.

Risk: Dependency ranges are not pinned to exact versions.

Mitigation: Pin and review dependencies before deployment, especially in environments that process sensitive meeting content.

## Reference(s):

- [Meeting Recorder Assistant on ClawHub](https://clawhub.ai/kaiyuelv/skills/meeting-recorder-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, JSON, TXT, and Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write transcript, audio, action-item, and meeting-minutes files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
