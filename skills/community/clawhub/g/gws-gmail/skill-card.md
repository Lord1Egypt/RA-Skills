## Description:

Gmail: Send, read, and manage email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Gmail commands and operate Gmail resources through the gws CLI, including sending, reading, triaging, forwarding, watching, and managing mailbox resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let the gws CLI access and modify Gmail data, including real mailbox state.

Mitigation: Install only for accounts where Gmail access is intended, and review the Google account and OAuth scopes configured for gws before use.

Risk: Send, settings, watch, forwarding, and reply operations can affect live email behavior.

Mitigation: Inspect command schemas before execution, review generated parameters, and require human approval for outbound or mailbox-changing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and appropriate Google Workspace or Gmail account authorization.]

## Skill Version(s):

1.0.14 (source: server release metadata); artifact metadata version 0.22.5

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
