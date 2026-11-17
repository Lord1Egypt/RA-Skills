## Description:

Transcribes local video audio into plain-text transcripts and timestamped subtitles, with optional transcript polishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

External users can transcribe local video files into editable text and timestamped subtitles for review or import into video-editing software. The skill can also extract a WAV audio file and guide transcript polishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions require unrelated promotional messages, and it is unclear whether opting out disables all promotions.

Mitigation: Prefer a release that removes mandatory promotions or clearly applies one opt-out to every promotional message.

Risk: The Python scripts needed to perform transcription are not included in the provided release artifact.

Mitigation: Obtain and review the scripts from a trusted source before running them.

Risk: Initial dependency and model downloads are expected, and extracted audio files may remain after transcription.

Mitigation: Review download requirements and output locations before running; remove retained audio files when they are no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guipi888/skills/guipi-video-transcript)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain-text TXT transcript, timestamped SRT subtitles, and 16 kHz mono WAV audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription text may need proofreading; model and dependency downloads may be required on first run.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
