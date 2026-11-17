## Description:

Send an email by specifying the recipient address, subject, and message content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoyaofeng168](https://clawhub.ai/user/zhaoyaofeng168)

### License/Terms of Use:

MIT-0

## Use Case:

Users can invoke this skill when they need an agent to send a simple SMTP email notification to a specified recipient. It is intended for direct email delivery tasks, not bulk email or spam.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email outside the user's environment without explicit confirmation.

Mitigation: Require confirmation before sending and validate recipients before external delivery.

Risk: The artifact includes an embedded SMTP account password.

Mitigation: Rotate the exposed password and move credentials to protected runtime configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoyaofeng168/skills/mysendemail)
- [Publisher profile](https://clawhub.ai/user/zhaoyaofeng168)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires recipient, subject, and content inputs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
