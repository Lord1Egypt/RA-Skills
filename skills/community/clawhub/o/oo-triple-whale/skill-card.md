## Description:

Search and read Triple Whale data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to query Triple Whale store metrics, customer journey attribution, and Data-Out results. The agent follows the action schema and returns the requested data for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions provide a downloaded installer whose contents are unverified.

Mitigation: Prefer a reviewed, preinstalled oo CLI; require approval before running any downloaded installer.

Risk: Triple Whale requests and returned business or customer data pass through OOMOL, and the hosted connector implementation is unverified.

Mitigation: Use the connector only where this data flow is acceptable, and limit requests to the store data and date range needed.

Risk: The CLI may automatically synchronize skills.

Mitigation: Review the synchronization behavior and disable it if it is not wanted.

## Reference(s):

- [Triple Whale](https://www.triplewhale.com)
- [Triple Whale API documentation](https://triplewhale.readme.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON connector requests and responses, summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action, store, and date range.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
