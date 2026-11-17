## Description:

Use the oo CLI to inspect ClickHouse schemas and execute SQL through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to inspect ClickHouse databases, review schemas, and run SQL through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote CLI installer, and the dependency's persistent managed-skill behavior has not been fully verified.

Mitigation: Verify the CLI release before installation, review its managed-skill behavior, and set OO_SKILLS_SYNC_DISABLED=1 if startup synchronization is unwanted.

Risk: SQL execution may affect ClickHouse data.

Mitigation: Use a connection with only the needed permissions and approve the exact SQL targets before execution.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClickHouse documentation: HTTP interface](https://clickhouse.com/docs/interfaces/http)
- [ClickHouse](https://clickhouse.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and connected ClickHouse database.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
