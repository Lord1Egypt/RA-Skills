## Description:

Unified Microsoft 365 skill for OpenClaw with modular features for Exchange Online (Email), SharePoint, OneDrive, and Planner, including webhook support for real-time notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felox63](https://clawhub.ai/user/felox63)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure and automate Microsoft Graph workflows for Exchange Online email, SharePoint, OneDrive, Planner, and webhook-triggered processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook and invoice-processing paths include unsafe shell command execution.

Mitigation: Replace shell command execution with non-shell argument passing before production use.

Risk: Webhook validation can be weak if secrets are optional, defaulted, or not checked for every notification.

Mitigation: Require strong webhook secrets and validate client state for every webhook item.

Risk: Telegram notification behavior can disclose Microsoft 365 or invoice-processing information to a third party.

Mitigation: Make Telegram notifications explicit and opt-in, and document what data is transmitted.

Risk: Persistent setup can leave PM2 processes, cron jobs, Microsoft Graph subscriptions, or temporary state behind.

Mitigation: Provide and run a teardown process that removes background services, subscriptions, and temporary state.

Risk: Microsoft Graph permissions can expose broad mailbox, SharePoint, OneDrive, and Planner access.

Mitigation: Grant only the smallest required scopes and restrict the app to specific mailboxes, sites, users, groups, and plans.

Risk: Unlocked dependencies can change installed code over time.

Mitigation: Lock dependencies and review updates before installation.

## Reference(s):

- [M365 Unified ClawHub Skill Page](https://clawhub.ai/felox63/skills/m365-unified)
- [felox63 Publisher Profile](https://clawhub.ai/user/felox63)
- [Webhook Integration Guide](docs/webhooks.md)
- [Microsoft Graph Webhooks Documentation](https://learn.microsoft.com/en-us/graph/webhooks)
- [Microsoft Graph Change Notifications](https://learn.microsoft.com/en-us/graph/change-notifications-overview)
- [Microsoft Graph Overview](https://learn.microsoft.com/en-us/graph/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Microsoft Graph API calls and environment configuration guidance; webhook automation requires external services and secrets.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
