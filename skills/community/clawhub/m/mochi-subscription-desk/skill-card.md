## Description:

Track software, memberships and service renewals, calculate cancellation deadlines, forecast costs by currency and queue due notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People managing recurring software, memberships and service charges can record subscriptions, review upcoming renewal and cancellation dates, forecast costs by currency, and prepare reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription records and renewal details are stored in the local workspace.

Mitigation: Keep the local subscription database and its workspace private.

Risk: A reminder could use the wrong recipient, timezone or frequency, or fail to reach its destination.

Mitigation: Specify the recipient, timezone and frequency, then verify reminder delivery.

Risk: A recorded cancellation deadline does not cancel the subscription automatically.

Mitigation: Review cancellation dates and cancel with the service yourself; verify any reminder schedule and delivery.

## Reference(s):

- [Input actions and subscription fields](references/input.md)
- [Host scheduling and notification delivery](references/notifications.md)
- [OpenClaw cron jobs guide](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON results with human-readable subscription summaries and reminder guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast totals stay separate by currency; no exchange rates are applied. Reminders require user-authorized host scheduling and delivery.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
