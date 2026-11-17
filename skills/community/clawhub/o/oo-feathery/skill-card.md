## Description:

Feathery (feathery.io). Use this skill for ANY Feathery request — reading, creating, updating, and deleting data. Whenever a task involves Feathery, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People building or managing Feathery forms and user data use this skill to inspect account information, forms, users, and submissions, and to create, update, or delete supported Feathery records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup requests remote code execution and may make broader changes to the agent environment without clearly explaining or confirming them.

Mitigation: Review the CLI installer separately before setup, prefer a verified pinned release, and decide whether to disable automatic skill synchronization across agent applications.

Risk: The connected Feathery account can expose account data and supports write and destructive actions.

Mitigation: Limit connected account access to the data needed and retain the required confirmations before changes or deletions.

## Reference(s):

- [Feathery](https://www.feathery.io/)
- [Feathery API documentation](https://api-docs.feathery.io/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; connector responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-action input and output schemas are obtained from the connected service; responses include data and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
