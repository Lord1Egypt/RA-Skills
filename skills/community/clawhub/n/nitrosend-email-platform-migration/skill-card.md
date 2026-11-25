## Description:

Guides agents through migrating email contacts and their consent statuses into Nitrosend, then rebuilding needed emails and automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

Email marketers and teams use this skill to move consent-aware contacts, lists, tags, and custom fields into Nitrosend, then recreate the email templates and automations they still need.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing contacts who have not subscribed to email marketing could create unintended subscriptions.

Mitigation: Import only subscribed contacts, preserve status or consent columns for the import to process, and confirm subscribed, unsubscribed, and blocked counts before sending.

Risk: Missing or incorrectly applied suppressions could allow email to reach bounced or complaint addresses.

Mitigation: Import unsubscribes, bounces, and complaints before contacts, verify sample suppression records, and stop if any address or blocking status is incorrect.

## Reference(s):

- [Email migration FAQ](https://docs.nitrosend.com/faq#contacts-and-migration)
- [ClawHub skill release](https://clawhub.ai/nitrosend/skills/nitrosend-email-platform-migration)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown guidance and Nitrosend tool requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes consent-aware migration steps and verification guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
