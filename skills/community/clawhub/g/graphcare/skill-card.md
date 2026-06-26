## Description: <br>
Structural database health scanner that audits schema topology for orphaned tables, missing indexes, nullable foreign keys, circular dependencies, and related issues across PostgreSQL, MySQL, and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nlr-ai](https://clawhub.ai/user/nlr-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use GraphCare to let an agent audit PostgreSQL, MySQL, or SQLite schema topology for structural issues and receive JSON health reports plus plain-language finding explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQLite scans may load an entire local database file despite metadata-only claims. <br>
Mitigation: Use least-privileged access and review before scanning SQLite databases with sensitive contents. <br>
Risk: Database connection strings are supplied to the MCP server during scans. <br>
Mitigation: Use credentials scoped to metadata inspection and avoid privileged production accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nlr-ai/graphcare) <br>
- [Project homepage from metadata](https://github.com/mind-protocol/graphcare) <br>
- [Mind Protocol](https://mindprotocol.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [JSON health reports and plain-language text explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include detected database type, table list, findings, metrics, severity, impact, and recommended fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
