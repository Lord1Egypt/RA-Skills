## Description:

Guides OpenClaw data warehouse table creation by helping users define workspace, table naming, fields, partitions, storage format, lifecycle settings, and DDL for ODS, DWD, DWS, DIM, and ADS layers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangyan0722](https://clawhub.ai/user/jiangyan0722)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to draft OpenClaw data warehouse CREATE TABLE DDL with consistent naming, field definitions, partition strategy, storage format, and TTL choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DDL may be incorrect for a specific production workspace or data governance policy.

Mitigation: Review the generated SQL, workspace, schema, partitioning, storage format, and lifecycle settings before running it.

Risk: The skill is written for Chinese-language DDL workflows, which may lead to misunderstandings for users outside that context.

Mitigation: Confirm table requirements and generated comments with a user who understands the target OpenClaw workflow and language context.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; generated SQL should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
