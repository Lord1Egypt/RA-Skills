## Description:

MeetingClaw transcribes uploaded meeting audio with Volcengine recording recognition and uses OpenClaw to generate structured meeting minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maginaaa2023](https://clawhub.ai/user/maginaaa2023)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn authorized meeting recordings into concise Markdown minutes with summaries, key points, and action items. It is intended for audio files that may be sent to Volcengine for transcription and then summarized by OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send readable local audio file paths to Volcengine and OpenClaw.

Mitigation: Use it only with recordings you are authorized to process with those services, and avoid passing arbitrary or unrelated local paths.

Risk: The MeetingClaw workspace cleanup behavior may remove older local files beyond what users expect.

Mitigation: Keep unrelated files out of the MeetingClaw workspace and review local retention behavior before running the skill.

Risk: Volcengine credentials are required for transcription.

Mitigation: Use narrowly scoped credentials and rotate or revoke them if they may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maginaaa2023/skills/meeting-claw)
- [Standard mode guide](references/standard_mode.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown meeting minutes and local saved files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured minutes may include a meeting topic, basic information, summary, key points, action items, and other important notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
