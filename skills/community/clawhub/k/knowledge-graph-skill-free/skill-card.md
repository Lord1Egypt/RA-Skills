## Description: <br>
知识图谱基础版 helps agents create, update, delete, query, import, export, and locally persist simple entity-relation knowledge graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and small teams use this skill to manage simple structured knowledge graphs for LLM apps, conversations, and agent workflows. It covers entity and relation CRUD, shallow neighbor queries, property filters, and local JSON or SQLite persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command-execution capability for work that mainly needs local graph reads and writes. <br>
Mitigation: Review before installing, restrict or monitor exec use where possible, and allow commands only for expected local graph operations. <br>
Risk: Exported graph data could be written outside intended local locations. <br>
Mitigation: Store exported graph data only in approved local paths and verify file destinations before writing or sharing graph data. <br>
Risk: Generated graph operations or query results may be incomplete or incorrect. <br>
Mitigation: Review operation results, validate entity and relation identifiers, and keep backups before update, delete, import, or export actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/knowledge-graph-skill-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, guidance] <br>
**Output Format:** [JSON operation results, Markdown guidance, and local JSON or SQLite export paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports create_entity, update_entity, delete_entity, create_relation, query_neighbors, query_by_property, export, and import actions; query depth is limited to 2.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
