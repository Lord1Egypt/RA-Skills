## Description:

A terminal utility for recording notification-related command entries locally and reviewing recent activity, status, search results, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and terminal users can use this skill to keep local plaintext records of notification-related commands and inspect or export those records. It should not be relied on for real alert delivery, scheduling, filtering, or delivery confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged as suspicious because the shipped script mainly stores arbitrary command inputs in local log files and does not implement the advertised scheduling, alert delivery, filtering, or delivery tracking.

Mitigation: Review the artifact before installation and treat it only as a local plaintext logging utility.

Risk: Notification content entered through the CLI may be stored in plaintext under ~/.local/share/notification.

Mitigation: Avoid entering secrets or sensitive notification content and inspect or remove ~/.local/share/notification after testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/notification)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain publisher profile](https://clawhub.ai/user/bytesagain3)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with local JSON, CSV, or plain text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local plaintext logs under ~/.local/share/notification.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
