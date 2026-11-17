## Description:

Hologres DDL schema design and table creation expert for generating CREATE TABLE statements, choosing storage formats, configuring table properties, designing partition tables, selecting data types, and optimizing schemas for query patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design Hologres table schemas, generate DDL, choose storage and indexing properties, and plan partitioning for expected query patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied Hologres commands can modify database state when run through hologres-cli.

Mitigation: Run in an isolated environment first, pin and review hologres-cli, and review target connections and DDL before using write-capable commands.

Risk: Partition lifecycle examples include DROP TABLE statements and automation that can delete data if applied to production targets.

Mitigation: Confirm exact targets, retention policy, backups, and a dry-run review before running any partition-drop example or automation.

Risk: Incorrect immutable table properties such as orientation, distribution key, clustering key, event time column, primary key, or partition column can require table recreation.

Mitigation: Gather query patterns, key columns, main filters, joins, data volume, and retention needs before generating final DDL.

## Reference(s):

- [Hologres Data Types Reference](references/data-types.md)
- [Hologres Partition Table Guide](references/partition-guide.md)
- [Hologres Table Properties Reference](references/table-properties.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Hologres DDL, table property recommendations, partition lifecycle guidance, and assumptions that should be reviewed before execution.]

## Skill Version(s):

0.2.0 (source: server release metadata and VERSION; package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
