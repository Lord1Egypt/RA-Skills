## Description: <br>
Hologres Schema Generator helps design Hologres DDL, table storage formats, partitioning, data types, and table properties for query-pattern-aware schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and database practitioners use this skill to generate and review optimized Hologres CREATE TABLE statements, storage choices, partitioning plans, and related schema guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or example CREATE, ALTER, DROP, and scheduled cleanup SQL can modify or permanently remove Hologres data. <br>
Mitigation: Review all generated SQL before execution, especially partition drops and lifecycle cleanup statements. <br>
Risk: The skill depends on hologres-cli executing against the configured Hologres account and database. <br>
Mitigation: Install hologres-cli only from a trusted source and verify the target account and database before running commands. <br>


## Reference(s): <br>
- [Hologres Data Types Reference](references/data-types.md) <br>
- [Hologres Partition Table Guide](references/partition-guide.md) <br>
- [Hologres Table Properties Reference](references/table-properties.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable database-changing SQL that should be reviewed before use.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
