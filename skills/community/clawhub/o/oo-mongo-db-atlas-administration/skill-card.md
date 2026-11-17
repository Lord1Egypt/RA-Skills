## Description:

Use the connected OOMOL account to list MongoDB Atlas projects and clusters or retrieve details for a specific project or cluster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to list Atlas projects and clusters or retrieve a specific project or cluster through their connected Atlas account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can persistently change other agents’ skills without this skill clearly explaining that behavior.

Mitigation: Review the CLI’s wider skill-management behavior, install a reviewed CLI release, and set OO_SKILLS_SYNC_DISABLED=1 before invoking it if you do not want automatic agent-skill changes.

## Reference(s):

- [MongoDB Atlas Administration API documentation](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/)
- [MongoDB Atlas overview](https://www.mongodb.com/products/platform/atlas-database)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-mongo-db-atlas-administration)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON results with shell-command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Atlas project and cluster information]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
