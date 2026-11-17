## Description:

Google Workspace Alert Center: Manage Workspace security alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:


## Use Case:

Developers and workspace administrators use this skill to inspect and operate Google Workspace Alert Center commands for listing, retrieving, deleting, undeleting, and configuring security alerts through the gws CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alert deletion, batch deletion, or settings updates may affect the wrong customer, alert, or retention state if parameters are incorrect.

Mitigation: Before mutation commands, confirm the target customer, alert IDs, and expected retention or recovery behavior.

Risk: The agent operates against Google Workspace Alert Center through configured gws credentials.

Mitigation: Install and use the skill only in environments where those credentials are intended for Alert Center operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-alertcenter)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and configured Google Workspace credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
