## Description:

Watch Singapore HDB resale transactions and get alerted only when new sales are registered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memeanalyst](https://clawhub.ai/user/memeanalyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users can monitor HDB resale registrations by town and flat type, receive alerts when new transactions appear, or search official resale records once.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: Actor runs and alerts incur charges on the user's Apify account.

Mitigation: Review the stated per-record and per-alert prices, result limit, and chosen check cadence before starting a watch.

Risk: The skill requires an Apify API token for account access.

Mitigation: Configure the user's token only in the authorized Apify plugin environment and keep it private.

## Reference(s):

- [Apify Singapore HDB Resale Monitor Actor](https://apify.com/magnova/sg-hdb-resale-monitor)
- [HDB Resale Watcher on ClawHub](https://clawhub.ai/memeanalyst/skills/hdb-resale-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries of HDB resale records and watch alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries can include transaction details and price ranges; actor runs may incur the charges stated in the skill documentation.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
