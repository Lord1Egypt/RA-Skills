## Description:

Mailtrap (mailtrap.io). Use this skill for ANY Mailtrap request — reading, creating, updating, and deleting data. Whenever a task involves Mailtrap, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Mailtrap inboxes, contacts, templates, sending domains, and projects through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to run a remote CLI installer that was not inspected.

Mitigation: Review and approve the CLI installation separately, using a verified release; consider OOMOL's access to Mailtrap data and the CLI's synchronization scope before proceeding.

## Reference(s):

- [Mailtrap API documentation](https://docs.mailtrap.io/developers/account-management/)
- [Mailtrap](https://mailtrap.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON API results with natural-language summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change or delete data require explicit user confirmation before execution.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter; confirmed by server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
