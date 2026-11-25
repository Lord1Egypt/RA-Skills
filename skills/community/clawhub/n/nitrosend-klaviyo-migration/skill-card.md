## Description:

Migrate from Klaviyo to Nitrosend: import profiles and lists exported from Klaviyo as CSV, keep unsubscribes and suppressions, then rebuild flows such as welcome series, abandoned cart and post-purchase as Nitrosend drafts and connect Shopify for store events. Use when moving email marketing from Klaviyo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams use this skill to move email subscribers, suppression states, and flow drafts from Klaviyo to Nitrosend while preserving consent and checking contact status before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing an entire account can subscribe contacts who did not opt in.

Mitigation: Import only subscribed profiles, keep the Email Marketing Consent column available to the import, and exclude anyone who never subscribed.

Risk: Unsubscribes, bounces, or complaints may receive the wrong suppression state, allowing unwanted email delivery.

Mitigation: Separate suppression exports by reason, apply unsubscribe or block-all settings as directed, and verify suppression records and counts before sending.

## Reference(s):

- [Nitrosend migration FAQ](https://docs.nitrosend.com/faq#contacts-and-migration)
- [Klaviyo Migration on ClawHub](https://clawhub.ai/nitrosend/skills/nitrosend-klaviyo-migration)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Markdown migration instructions with API tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sequenced workflow for contact imports, suppression checks, and inactive flow drafts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
