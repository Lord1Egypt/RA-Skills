## Description:

Transcribe speech from videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to transcribe speech from video files and save transcription results as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video files may contain sensitive speech or personal data that could be sent to an unspecified transcription provider.

Mitigation: Confirm the transcription service and its data handling terms before use, and avoid processing sensitive recordings unless that provider is approved.

Risk: The referenced script is not included in the artifact, so runtime behavior and provider selection cannot be verified from the skill package alone.

Mitigation: Inspect the script and required dependencies before installation or execution.

Risk: Broad trigger conditions may cause the skill to be used for video-related requests where transcription is not intended.

Mitigation: Narrow activation and usage guidance to explicit video transcription tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-video-transcriber)
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRANSCRIPTION_API_KEY configuration and returns transcription results as JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
