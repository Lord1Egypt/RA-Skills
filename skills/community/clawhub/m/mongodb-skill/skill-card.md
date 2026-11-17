## Description:

MongoDB 文档数据库管理技能。通过自然语言查询、管理 MongoDB，支持文档查询、聚合操作、索引管理、地理空间查询等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and backend engineers use this Chinese-language skill to translate MongoDB administration requests into queries, aggregation pipelines, document updates, index operations, geospatial queries, and backup or restore commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MongoDB write, restore, transaction, or index commands can change or remove production data if run without review.

Mitigation: Review every generated command before execution, test on non-production data when possible, and keep a verified backup before destructive or restore operations.

Risk: Database credentials used with generated commands may have broader access than the task requires.

Mitigation: Use least-privilege MongoDB users and avoid exposing credentials in shared prompts, logs, or shell history.

Risk: Unpinned client dependencies can reduce reproducibility across environments.

Mitigation: Install dependencies in an isolated environment and pin PyMongo or MongoDB client versions when repeatable behavior is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryanlee-gemini/skills/mongodb-skill)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [MongoDB Query Operators](https://www.mongodb.com/docs/manual/reference/operator/)
- [MongoDB Aggregation Pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, shell command, and connection-string examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are command and query proposals that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
