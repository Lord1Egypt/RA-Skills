## Description: <br>
Lucid Skill connects Excel, CSV, MySQL, and PostgreSQL data sources so agents can explore schemas, discover semantics and joins, and answer questions with read-only SQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenkang-xie](https://clawhub.ai/user/wenkang-xie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to connect local files or supported databases, inspect schemas and semantic metadata, discover joins, and answer business questions with read-only SQL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads connected data sources and may expose or summarize sensitive records through query, profile, describe, and search outputs. <br>
Mitigation: Connect only approved datasets, use read-only database accounts, and avoid regulated or highly sensitive data unless local review confirms the exposure is acceptable. <br>
Risk: The skill caches metadata and sample values locally, which can retain information from connected datasets after a session. <br>
Mitigation: Set LUCID_DATA_DIR to a controlled location, apply appropriate filesystem protections, and clear the directory when cached samples should not persist. <br>
Risk: Database credentials are required for MySQL and PostgreSQL connections and can be exposed through shell history if entered directly on the command line. <br>
Mitigation: Prefer least-privilege accounts and avoid putting real passwords in reusable command history or shared logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenkang-xie/lucid-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/wenkang-xie) <br>
- [Command Reference](references/commands.md) <br>
- [Semantic JSON Schema](references/json-schema.md) <br>
- [Workflow Guide](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON by default, with Markdown or CSV query results when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only SQL execution with automatic row limits and truncation reporting] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
