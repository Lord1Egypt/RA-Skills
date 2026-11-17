## Description:

Operate NocoDB by inspecting connector schemas and running actions through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect NocoDB bases, tables, views, and records, and to create, update, or delete data through a connected NocoDB account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a changeable remote installer, and the linked CLI documentation describes automatic changes to other assistants’ installed skills.

Mitigation: Review and install a pinned CLI release; review or disable automatic skill synchronization before use.

Risk: Available actions include writes and destructive data changes in NocoDB.

Mitigation: Connect only the needed NocoDB resources and retain approval for writes and deletions.

## Reference(s):

- [NocoDB homepage](https://nocodb.com)
- [NocoDB API documentation](https://docs.nocodb.com/0.109.7/developer-resources/accessing-apis/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [NocoDB skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-nocodb)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON action results and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read or change data in the connected NocoDB account.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
