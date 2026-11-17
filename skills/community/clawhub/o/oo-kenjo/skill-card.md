## Description:

Kenjo (kenjo.io). Use this skill for ANY Kenjo request — reading, creating, updating, and deleting data. Whenever a task involves Kenjo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Kenjo users use this skill to read and manage office data and to list companies, departments, calendars, and offices through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs an unverified remote installer without approval or a clear explanation of its broader local effects.

Mitigation: Review the CLI installation separately, use a verified release, and review or disable automatic skill synchronization before setup.

Risk: Actions run against the connected Kenjo account, and office updates or deletions change account data.

Mitigation: Connect only the intended account and retain the skill's confirmation requirements for updates and deletions.

## Reference(s):

- [Kenjo API documentation](https://kenjo.readme.io/)
- [Kenjo homepage](https://www.kenjo.io/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-kenjo)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands, JSON requests and responses, and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
