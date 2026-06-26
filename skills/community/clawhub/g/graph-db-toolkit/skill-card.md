## Description: <br>
Graph database toolkit for Neo4j and Cypher-based graph analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to design Neo4j graph schemas, build Cypher queries, run CRUD operations, and apply graph analytics to knowledge graphs, relationship analysis, recommendation systems, and network workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database-write or destructive graph operations could modify or delete Neo4j data. <br>
Mitigation: Use least-privileged database credentials and test or back up databases before running destructive operations. <br>
Risk: Untrusted input in labels, field names, WHERE clauses, or raw Cypher strings could lead to unsafe queries. <br>
Mitigation: Review generated Cypher and avoid passing untrusted user input directly into query structure or raw Cypher strings. <br>


## Reference(s): <br>
- [Graph DB Toolkit on ClawHub](https://clawhub.ai/kaiyuelv/graph-db-toolkit) <br>
- [Cypher Cheatsheet](references/cypher_cheatsheet.md) <br>
- [Neo4j Design Patterns](references/neo4j_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and Cypher code snippets, shell commands, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database-write or destructive Cypher operations that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
