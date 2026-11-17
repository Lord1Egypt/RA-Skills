## Description:

Control the iPlay media player to play videos or streams from URLs, including YouTube, Bilibili, and direct media links such as mp4 and m3u8.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saltpi](https://clawhub.ai/user/saltpi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to open videos or streams in the local iPlay desktop media player from supported URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens user-provided media URLs in the local iPlay application.

Mitigation: Only play URLs from trusted sources and review agent-proposed media links before execution.

Risk: The helper triggers playback asynchronously and does not monitor playback status.

Mitigation: Confirm playback and errors in the iPlay application when reliable completion status is required.

Risk: On Windows, the helper uses a shell command to launch the iPlay URI.

Mitigation: Prefer a future helper version that avoids shell=True, and install only when this local launch behavior is acceptable.

## Reference(s):

- [iPlay homepage](https://iplay.saltpi.cn)
- [ClawHub iPlay skill page](https://clawhub.ai/saltpi/skills/iplay)
- [Publisher profile: saltpi](https://clawhub.ai/user/saltpi)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text with shell command examples and helper status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a local iPlay installation; playback is triggered asynchronously and status is not monitored.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
