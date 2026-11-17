## Description:

Operate Softr databases and records through the oo CLI using a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Softr databases, tables, and records, and to create, update, or delete records through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may install additional agent skills at startup, a broader effect not described by this skill.

Mitigation: Review the CLI before installation; set OO_SKILLS_SYNC_DISABLED=1 before invoking oo if startup skill changes are unwanted.

Risk: Softr write and delete actions can change or permanently remove records.

Mitigation: Limit the connected Softr permissions and confirm the exact payload and effect before write or delete actions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Softr homepage](https://www.softr.io/)
- [Softr Database API documentation](https://docs.softr.io/softr-api/softr-database-api)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Text responses, oo CLI commands, and JSON payloads or results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected Softr action; write and delete actions require approval.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
