## Description:

Operate SecurityScorecard through an OOMOL-connected account for reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

SecurityScorecard users use the skill to inspect company scores, security factors, score history, and portfolio data through an OOMOL-connected account. They can also create or update portfolios and manage company membership, with confirmation required for changes and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can synchronize persistent skills across agents, a side effect not explained in the skill instructions.

Mitigation: Review the CLI installation, use a verified release, and consider disabling startup synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: The connected account is mediated by OOMOL, and some actions change or delete SecurityScorecard data.

Mitigation: Use appropriately limited credentials and retain the skill's confirmation requirements for changes and deletion.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [SecurityScorecard](https://securityscorecard.com/)
- [SecurityScorecard API documentation](https://api.securityscorecard.io/api-docs)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON results with concise setup and safety guidance; inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected SecurityScorecard account and the selected action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
