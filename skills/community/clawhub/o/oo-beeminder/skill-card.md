## Description:

Connects an OOMOL-connected Beeminder account for reading and managing goals and datapoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can inspect Beeminder account information and manage goals and datapoints through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may execute an unverified CLI installer and introduce broader agent changes without separate approval.

Mitigation: Review and version-pin the CLI installation; disable automatic bundled-skill synchronization unless needed.

Risk: Connecting Beeminder entrusts OOMOL with the API key and requested operations.

Mitigation: Connect only the intended account and review each requested operation; follow the skill's confirmation safeguards for writes and deletions.

Risk: The hosted connector was not verified by this artifact review.

Mitigation: Review the connector and its requested access before connecting the account.

## Reference(s):

- [Beeminder](https://www.beeminder.com)
- [Beeminder API documentation](https://api.beeminder.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON connector results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Beeminder goal and datapoint data or results of requested changes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
