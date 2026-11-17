## Description:

Plain (plain.com). Use this skill for ANY Plain request — reading, creating, and updating data. Whenever a task involves Plain, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Plain customer records can search for and retrieve customers, or create and update a customer through their connected Plain account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructs users to run a remote CLI installer, and the installer and remote connector were not audited.

Mitigation: Install the CLI separately from a verified, pinned release before allowing the skill to run.

Risk: Actions use the connected Plain account and can change customer records.

Mitigation: Connect only the intended Plain account and review each customer change; decide whether to allow automatic synchronization of agent skills.

## Reference(s):

- [Plain](https://www.plain.com)
- [Plain API documentation](https://www.plain.com/docs/graphql/introduction)
- [oo CLI repository (referenced by the skill)](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands and JSON request/response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plain customer records and action results; customer updates require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
