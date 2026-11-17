## Description:

Mendeley (mendeley.com). Use this skill for ANY Mendeley request — reading, creating, updating, and deleting data. Whenever a task involves Mendeley, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the agent to search Mendeley's public catalog and read or manage documents in their authorized Mendeley library. The skill provides the commands and request payloads for those actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded software without a separate approval step, and the installer's exact effects could not be verified.

Mitigation: Review and separately approve a verified CLI installation, and check its automatic agent-skill synchronization settings before setup.

Risk: The skill can change or permanently delete records in the connected Mendeley library.

Mitigation: Fetch the live action schema before preparing a request, then confirm the exact payload and target with the user before any write or destructive action.

## Reference(s):

- [Mendeley API documentation](https://dev.mendeley.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Mendeley](https://www.mendeley.com/)
- [Mendeley skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-mendeley)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON request payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read, write, and destructive library actions; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
