## Description:

Headless Google Meet bot that joins meetings and captures live captions as transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumansid](https://clawhub.ai/user/sumansid)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to join authorized Google Meet sessions, capture live-caption transcripts, retrieve meeting summaries, and send meeting screenshots when visual context is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can join meetings, capture transcripts, take screenshots, and save a reusable Google session on disk.

Mitigation: Use it only for meetings where bot attendance, recording, transcription, and screenshot capture are authorized; protect or delete ~/.openutter/auth.json when it is no longer needed.

Risk: Server security evidence reports a confirmed shell-command injection risk.

Mitigation: Avoid untrusted channel or target values, prefer pinned local dependencies, and review execution paths before using the skill in sensitive environments.

Risk: Meeting transcripts and screenshots may contain sensitive content.

Mitigation: Limit access to the local OpenUtter workspace and review transcript or image contents before sharing them outside the meeting context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumansid/skills/openutter)
- [OpenUtter homepage](https://github.com/sumansid/openutter)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, transcript text, status messages, and screenshot file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates meeting transcript text files, screenshot images, and optional saved browser session files on the local machine.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
