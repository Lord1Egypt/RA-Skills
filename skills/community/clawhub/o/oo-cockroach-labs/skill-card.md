## Description:

Connects to CockroachDB Cloud to retrieve information about organizations, clusters, regions, databases, nodes, and SQL users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database administrators use the skill to inspect CockroachDB Cloud organizations, clusters, regions, databases, nodes, and SQL users through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run an unverified remote installer and make broader local changes to agent skills.

Mitigation: Review setup steps before use; prefer a separately reviewed, version-pinned oo CLI installation and consider disabling automatic skill synchronization.

Risk: A connected account may expose more CockroachDB Cloud access than the read actions need.

Mitigation: Use a Cockroach Labs connection with read-only permissions.

## Reference(s):

- [CockroachDB Cloud API documentation](https://www.cockroachlabs.com/docs/api/cloud/v1.html)
- [Cockroach Labs](https://www.cockroachlabs.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured connector results with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected read action and the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
