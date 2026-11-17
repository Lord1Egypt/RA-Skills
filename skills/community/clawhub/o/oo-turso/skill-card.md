## Description:

Turso (turso.tech). Use this skill for ANY Turso request — reading, creating, updating, and deleting data. Whenever a task involves Turso, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect Turso organizations, groups, databases, and locations, create groups and databases, and delete databases through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs downloaded code without a separate approval step; the installers and hosted connector implementation remain unverified.

Mitigation: Review setup before installing. Prefer a verified, fixed oo CLI version installed under your control, and review or disable automatic skill synchronization.

Risk: Database changes can affect connected Turso resources.

Mitigation: Connect only the Turso permissions needed and retain the required approvals for database changes.

## Reference(s):

- [Turso API quickstart](https://docs.turso.tech/api-reference/quickstart)
- [Turso](https://turso.tech)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Turso skill on ClawHub](https://clawhub.ai/oomol/skills/oo-turso)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and results, with shell commands shown in Markdown code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include returned data and an execution ID. Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
