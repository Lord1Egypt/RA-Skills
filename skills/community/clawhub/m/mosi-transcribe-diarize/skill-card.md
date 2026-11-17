## Description:

MOSI Transcribe Diarize uses MOSI Studio to transcribe URL, local file, or Base64 audio into timestamped, speaker-labeled JSON and text outputs for meetings, interviews, and multi-speaker conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkkb473](https://clawhub.ai/user/mkkb473)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and workflow agents use this skill to submit audio or video to MOSI Studio and generate diarized transcripts for meeting notes, interviews, and multi-speaker conversation review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio or video content is sent to MOSI Studio for transcription and may contain confidential or sensitive speech.

Mitigation: Use the skill only with recordings approved for MOSI Studio processing and avoid confidential recordings unless that service is approved for the data.

Risk: Transcript output files may contain sensitive speech content on the local filesystem.

Mitigation: Choose output paths carefully and handle generated JSON, segment, and by-speaker transcript files according to the user's data handling requirements.

## Reference(s):

- [MOSI Studio](https://studio.mosi.cn)
- [MOSI Studio transcription endpoint](https://studio.mosi.cn/v1/audio/transcriptions)
- [ClawHub skill page](https://clawhub.ai/mkkb473/skills/mosi-transcribe-diarize)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON plus plain-text transcript files and concise command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes raw JSON, segment timeline text, and by-speaker summary text to local output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
