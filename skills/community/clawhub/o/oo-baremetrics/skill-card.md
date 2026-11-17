## Description:

Use your OOMOL-connected Baremetrics account to read, create, update, and cancel records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Baremetrics account can inspect sources, charges, customers, plans, and subscriptions, and create or update records or cancel subscriptions through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute a remote installer whose contents were unavailable for review.

Mitigation: Use an integrity-verified oo CLI release, require separate approval before installation, and review its automatic skill-installation behavior.

Risk: Create, update, and cancellation actions can change Baremetrics records.

Mitigation: Confirm the exact target, payload, and effect before writes, and get explicit approval before cancelling a subscription.

## Reference(s):

- [Baremetrics API reference](https://developers.baremetrics.com/reference)
- [Baremetrics](https://baremetrics.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON data, Text, Guidance]

**Output Format:** [JSON responses with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Baremetrics account and the action's live schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
