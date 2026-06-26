## Description: <br>
Runs openCypher against Ladybug DB with schema-first DDL, Python sync/async execution, CALL procedures, full-text search, and Neo4j divergence notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trenza1ore](https://clawhub.ai/user/trenza1ore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to write, debug, and migrate Ladybug openCypher queries, including schema-first DDL, Python execution, imports, CALL procedures, full-text search, and Neo4j behavior differences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-run Cypher can modify the selected Ladybug database. <br>
Mitigation: Review Cypher for CREATE, COPY, LOAD, DROP, SET, and other mutating operations, confirm the .lbug path, and back up important databases before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/trenza1ore/ladybug-opencypher) <br>
- [API reference](references/api-reference.md) <br>
- [Workflow patterns](references/workflow-patterns.md) <br>
- [openCypher](https://opencypher.org/) <br>
- [Ladybug vs Neo4j](https://docs.ladybugdb.com/cypher/difference/) <br>
- [Ladybug Python API](https://docs.ladybugdb.com/client-apis/python/) <br>
- [Ladybug import data](https://docs.ladybugdb.com/import/) <br>
- [Ladybug full-text search](https://docs.ladybugdb.com/extensions/full-text-search/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Cypher, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that execute user-provided Cypher against a selected Ladybug database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
