## Description:

Helps OpenClaw agents notify people through PingRoom, request answers or approvals, share live progress, and receive incoming pings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingroom](https://clawhub.ai/user/pingroom)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use PingRoom to send phone notifications, request human decisions before actions, and follow replies or live progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, files, links, and locations are shared with PingRoom and the paired person's phone.

Mitigation: Send only agreed-upon content; confirm before sharing files or locations.

Risk: A leaked token or credential could allow unintended access to the connected account.

Mitigation: Keep the token and credential file tightly scoped and private.

Risk: Urgent pings or room-management changes can interrupt people or alter shared rooms.

Mitigation: Confirm intent before sending urgent pings or changing room settings.

## Reference(s):

- [PingRoom OpenClaw guide](https://pingroom.io/connect-openclaw.md)
- [PingRoom skill on ClawHub](https://clawhub.ai/pingroom/skills/pingroom)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can relay notification status and human responses.]

## Skill Version(s):

1.2.3

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
