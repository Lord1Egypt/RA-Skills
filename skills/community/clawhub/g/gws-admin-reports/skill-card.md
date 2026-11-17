## Description:

Google Workspace Admin SDK: Audit logs and usage reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Google Workspace administrators and operators use this skill to guide agent use of the gws CLI for Admin SDK audit logs, usage reports, activity watches, and report discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged gws credentials can expose sensitive Google Workspace audit logs and usage reports.

Mitigation: Install and use the skill only with intended Google Workspace admin credentials and review the shared gws authentication and security rules before use.

Risk: Activity watch channels can subscribe to sensitive tenant activity notifications.

Mitigation: Inspect gws schema output and confirm watch parameters before starting or stopping report notification channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-admin-reports)
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured gws CLI and appropriate Google Workspace admin permissions.]

## Skill Version(s):

1.0.13 (source: ClawHub release evidence; skill metadata version: 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
