## Description:

Inspects Mermail workspace usage and helps authorized administrators manage access, domains, mailboxes, settings, storage, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Mermail workspace administrators use this skill to review usage and plan limits, manage members and email resources, and inspect or change webhook subscriptions with appropriate approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative changes can alter member access, domains, mailboxes, and workspace settings.

Mitigation: Confirm the exact workspace and target, preview intended changes, obtain required approval, and verify the resulting state.

Risk: Webhook actions can transmit selected email content to an external destination or invalidate an existing signing secret.

Mitigation: Review the destination host and event set, require explicit approval before changes or deliveries, and keep URLs, authorization values, and secrets out of summaries.

Risk: Mailbox provisioning consumes credits, and uncertain retries can duplicate externally visible actions.

Mitigation: Check for an existing mailbox first, disclose the provision cost, and inspect state before retrying uncertain actions with unchanged identifiers.

## Reference(s):

- [Mermail AI skills documentation](https://docs.mermail.app/ai/skills)
- [ClawHub skill release](https://clawhub.ai/mermail/skills/mermail-administer-workspace)
- [Workspace administration tools](references/tools.md)
- [Workspace AI credits](references/ai-credits.md)
- [Workspace webhooks](references/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown usage reports, change proposals, and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies exact targets and approval or verification status without repeating credentials or webhook secrets.]

## Skill Version(s):

1.2.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
