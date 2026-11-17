## Description:

Use an OOMOL-connected account to search and read RepairShopr customer and ticket data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support staff and service teams can look up the connected RepairShopr account's current user, customer records, and ticket details or lists. The skill is intended for read-only requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded CLI installers, and the remote installer was unavailable for inspection.

Mitigation: Review and approve the CLI installation separately before setup; inspect the installer changes when available.

Risk: The connected RepairShopr account provides access to customer and ticket data through OOMOL.

Mitigation: Connect only an authorized RepairShopr account and request only the information needed for the task.

## Reference(s):

- [RepairShopr](https://www.repairshopr.com)
- [RepairShopr API documentation](https://api-docs.repairshopr.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [RepairShopr skill page](https://clawhub.ai/oomol/skills/oo-repairshopr)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [RepairShopr records as JSON with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups for the connected account, customers, and tickets.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
