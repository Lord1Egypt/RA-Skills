## Description:

PlanetScale (planetscale.com). Use this skill for ANY PlanetScale request — reading, creating, updating, and deleting data. Whenever a task involves PlanetScale, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill through their connected OOMOL account to inspect PlanetScale organizations, databases, and branches, and to create or delete databases and branches. It guides the agent to check each action's live schema and seek confirmation before write or destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote code and add agent skills without clearly explaining those changes.

Mitigation: Review the CLI installation before allowing automatic setup, disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED if needed, and use a restricted PlanetScale connection.

## Reference(s):

- [PlanetScale API documentation](https://planetscale.com/docs/api/reference/getting-started-with-planetscale-api)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Connector requests and results with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
