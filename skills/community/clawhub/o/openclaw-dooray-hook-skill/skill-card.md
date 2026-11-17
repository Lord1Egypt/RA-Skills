## Description:

Send automated notifications to Dooray! messenger channels via webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iizs](https://clawhub.ai/user/iizs)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to send plain-text status notifications from an OpenClaw agent to configured Dooray chat rooms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured webhook destinations can receive messages and webhook tokens act as credentials.

Mitigation: Install only when the OpenClaw config is trusted and controlled, use genuine Dooray webhook URLs, and protect the config file permissions.

Risk: Disabling TLS verification can expose messages or webhook tokens if misconfigured.

Mitigation: Keep verify_ssl set to true and rotate any webhook token that may have been used with TLS verification disabled.

## Reference(s):

- [Dooray Incoming Webhook API Reference](artifact/references/dooray-api.md)
- [Dooray](https://dooray.com)
- [Dooray Helpdesk](https://helpdesk.dooray.com/)
- [ClawHub Skill Page](https://clawhub.ai/iizs/skills/openclaw-dooray-hook-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text notifications and Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends plain-text Dooray webhook messages to configured rooms; Dooray webhook URLs are treated as credentials.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
