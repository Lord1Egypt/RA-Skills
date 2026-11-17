## Description:

Search and read Beehiiv posts, publications, and subscriptions through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

An agent uses this skill to retrieve Beehiiv posts, publication details, and subscription records for people managing a Beehiiv account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI recovery may run a changing remote installer without a clear approval step.

Mitigation: Review and approve CLI installation separately, use a pinned and verified release, and keep the Beehiiv connection appropriately scoped.

Risk: The connected account can provide access to subscriber data.

Mitigation: Use an appropriately scoped Beehiiv connection and retrieve only the data needed for the task.

## Reference(s):

- [Beehiiv API documentation](https://developers.beehiiv.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON data with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields depend on the selected Beehiiv read action.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
