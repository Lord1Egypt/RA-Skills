## Description:

Google Workspace Events: Renew/reactivate Workspace Events subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Google Workspace administrators use this skill to get agent guidance and gws CLI commands for renewing or reactivating Google Workspace Events subscriptions, either by subscription name or in bulk within a time window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk renewal with `--all` or unattended cron scheduling can keep Google Workspace Events subscriptions active automatically.

Mitigation: Review the shared gws authentication and security documentation, scope `--all` with `--within`, and confirm renewal automation is intended before scheduling it.

Risk: The skill depends on an existing local `gws` CLI installation and its configured Google Workspace access.

Mitigation: Install it only in environments where `gws` is already approved and configured with the intended account permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-events-renew)
- [gws shared auth and global flags](../gws-shared/SKILL.md)
- [gws events command group](../gws-events/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI; examples cover renewing one subscription by name or renewing all subscriptions within a selected time window.]

## Skill Version(s):

1.0.12 (source: server release metadata; SKILL.md metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
