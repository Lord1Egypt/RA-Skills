## Description:

Dev.to (dev.to). Use this skill for ANY Dev.to request — reading, creating, and updating data. Whenever a task involves Dev.to, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read Dev.to articles, tags, videos, and profiles, and to create or update articles through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI may run unverified software and introduce changes to other agents' skills.

Mitigation: Review the CLI release and dependency setup before installing; set OO_SKILLS_SYNC_DISABLED=1 if you do not want automatic changes to other agents' skills.

Risk: Connecting Dev.to authorizes OOMOL-mediated account operations, including article creation and edits.

Mitigation: Retain approval for article changes and review the action schema and payload before running them.

## Reference(s):

- [Dev.to](https://dev.to)
- [Forem API documentation](https://developers.forem.com/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON request payloads and connector response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected Dev.to account and requested action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
