## Description:

Transcribe meetings with SenseAudio ASR speaker diarization, timestamps, and meeting-note extraction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers use this skill to transcribe recorded or live meetings with SenseAudio ASR, then produce speaker-separated transcripts, local meeting notes, decisions, action-item candidates, and timeline-friendly outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting recordings, transcripts, and the SenseAudio API key are sent to SenseAudio during transcription.

Mitigation: Use the skill only when the organization is comfortable with that provider path, confirm participant permission for confidential meetings, and review provider retention terms before processing sensitive audio.

Risk: The sample helper enables diarization, sentiment, and word-level timestamps, which can increase the sensitivity and granularity of generated meeting data.

Mitigation: Enable sentiment, diarization, and word-level timestamps only when explicitly needed for the meeting workflow.

Risk: The declared Python dependencies are not pinned in the release evidence.

Mitigation: Pin dependency versions before using the skill in a controlled or production environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/meetingsummarizer)
- [Publisher Profile](https://clawhub.ai/user/scikkk)
- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key)
- [SenseAudio HTTP Transcription Endpoint](https://api.senseaudio.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helper code and text-friendly transcript, notes, JSON, or CSV output options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include speaker-separated transcripts, timestamps, summaries, decisions, action-item candidates, speaker statistics, and optional sentiment timelines.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
