## Description:

Handles time-limited joining and leaving of group conversations on messaging platforms such as WhatsApp, Signal, and Telegram when the owner tags the agent into a group chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanblanchfield](https://clawhub.ai/user/seanblanchfield)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an owner-invited agent participate in a specific messaging-platform group for a bounded time window, then return the group to mention-required mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Group chat access could remain open longer than intended if owner or group policies are misconfigured or the scheduled close action fails.

Mitigation: Confirm OpenClaw owner and group policies before use, keep activation windows short, and verify mention-required mode is restored when the window closes.

Risk: Temporarily disabling mention requirements makes the agent eligible to participate in the selected group without every message mentioning it.

Mitigation: Open access only for the owner-approved group ID, and close early or replace the scheduled close action when the owner requests a change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanblanchfield/skills/group-activation)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Natural-language responses with configuration changes and scheduled close actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-limited group access; default duration is 30 minutes if unspecified.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
