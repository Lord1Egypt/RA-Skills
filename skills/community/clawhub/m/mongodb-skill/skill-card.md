## Description: <br>
MongoDB 文档数据库管理技能。通过自然语言查询、管理 MongoDB，支持文档查询、聚合操作、索引管理、地理空间查询等功能。当用户提到 MongoDB、NoSQL、文档数据库时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and backend engineers use this skill to draft MongoDB queries, aggregation pipelines, document updates, geospatial queries, index operations, and backup or restore commands from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MongoDB guidance can include bulk updates, deletes, index drops, restores, or schema-changing actions that affect live data. <br>
Mitigation: Review generated commands before execution, use read-only or least-privilege accounts by default, avoid exploratory prompts against production databases, and require explicit confirmation plus backups or matched-count review before destructive operations. <br>
Risk: Database credentials or connection strings could be exposed through prompts or shell history. <br>
Mitigation: Keep credentials out of prompts and command history, and use sanitized connection strings or environment-specific secret handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryanlee-gemini/mongodb-skill) <br>
- [MongoDB Official Documentation](https://www.mongodb.com/docs/) <br>
- [MongoDB Query Operators](https://www.mongodb.com/docs/manual/reference/operator/) <br>
- [MongoDB Aggregation Pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with MongoDB query examples, JavaScript snippets, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review before executing generated database-changing commands] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
