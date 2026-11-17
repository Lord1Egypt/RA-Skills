## Description:

Kit (kit.com). Use this skill for ANY Kit request — reading, creating, and updating data. Whenever a task involves Kit, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kit account operators use this skill to read Kit account, subscriber, form, and tag data, and to create or update subscribers through the connected Kit account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions direct users to install the oo CLI without a separate approval step, and the remote installer has not been verified.

Mitigation: Review and approve CLI installation separately, using a verified release where available.

Risk: Kit operations pass through OOMOL, while the hosted connector implementation has not been verified.

Mitigation: Understand that requests pass through OOMOL, and review the action and its effects before running it; retain the skill's confirmation requirement for subscriber changes.

## Reference(s):

- [Kit API documentation](https://developers.kit.com/api-reference/overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Kit](https://kit.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Kit data; subscriber creation and updates require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
