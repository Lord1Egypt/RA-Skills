## Description:

Transcribes local meeting recordings into timestamped transcripts, subtitles, and Markdown notes with action-item candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyeque](https://clawhub.ai/user/iyeque)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents handling authorized meetings, interviews, calls, lectures, or voice notes use this skill to create local transcripts, subtitles, and notes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings and generated transcripts may contain private information.

Mitigation: Process only recordings you are authorized to use, keep outputs inside the workspace, and avoid public sharing.

Risk: Whisper installation and first-run model downloads may require network access.

Mitigation: Plan for the dependency and pre-download a model when operating without network access.

Risk: Automatic transcripts and action-item candidates may be inaccurate.

Mitigation: Review the timestamped transcript before relying on notes or assigning action items.

## Reference(s):

- [Meeting Transcription on ClawHub](https://clawhub.ai/iyeque/skills/iyeque-meeting-transcription)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Markdown]

**Output Format:** [Local transcript JSON, SRT subtitles, and Markdown notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timestamped segments and deterministic action-item candidates; outputs stay in a workspace directory.]

## Skill Version(s):

0.1.0 (source: skill metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
