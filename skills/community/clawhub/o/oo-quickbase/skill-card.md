## Description:

Quickbase (quickbase.com). Use this skill for ANY Quickbase request — reading, creating, updating, and deleting data. Whenever a task involves Quickbase, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business teams use this skill to inspect Quickbase apps, tables, fields, and records, and to create, update, or delete records through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs an unverified remote installer, and the CLI may install or refresh other agent skills.

Mitigation: Review and install a verified CLI release; set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization when appropriate.

Risk: Quickbase write and deletion actions can change or remove records.

Mitigation: Connect only the required Quickbase permissions, review each proposed payload and effect, and get user approval before running these actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)
- [Quickbase API documentation](https://developer.quickbase.com/auth)
- [Quickbase](https://www.quickbase.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live action schemas are required before constructing requests; writes and deletions require user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
