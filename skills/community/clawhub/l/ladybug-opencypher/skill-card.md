## Description:

Runs openCypher against Ladybug DB with schema-first DDL, Python sync/async execution, CALL procedures, full-text search, and Neo4j divergence notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trenza1ore](https://clawhub.ai/user/trenza1ore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, debug, and migrate Ladybug openCypher queries, including schema-first DDL, imports, Python execution, CALL procedures, and full-text search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or supplied Cypher may modify a local Ladybug database through DDL, COPY/LOAD, CALL procedures, or FTS-related operations.

Mitigation: Review each Cypher statement before execution and run changes against a disposable or backed-up database when possible.

Risk: COPY, LOAD, and FTS/httpfs-related behavior may read local or remote files according to Ladybug behavior.

Mitigation: Use explicit trusted paths and review file-accessing queries before running helper scripts or Python snippets.

Risk: Neo4j-style assumptions can produce different Ladybug results because schema, DDL, MATCH semantics, and unsupported clauses differ.

Mitigation: Check Ladybug documentation and the bundled workflow patterns for walk/trail behavior, variable-length bounds, unsupported clauses, and CALL-based catalog procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trenza1ore/skills/ladybug-opencypher)
- [ClawHub publisher profile](https://clawhub.ai/user/trenza1ore)
- [Ladybug Python & Cypher API reference](references/api-reference.md)
- [Ladybug workflow patterns](references/workflow-patterns.md)
- [openCypher](https://opencypher.org/)
- [Ladybug vs Neo4j](https://docs.ladybugdb.com/cypher/difference/)
- [Ladybug Python API](https://docs.ladybugdb.com/client-apis/python/)
- [Ladybug generated Python reference](https://api-docs.ladybugdb.com/python)
- [Ladybug create table](https://docs.ladybugdb.com/cypher/data-definition/create-table/)
- [Ladybug import data](https://docs.ladybugdb.com/import/)
- [Ladybug full-text search](https://docs.ladybugdb.com/extensions/full-text-search/)
- [Ladybug MATCH](https://docs.ladybugdb.com/cypher/query-clauses/match)
- [Ladybug CALL](https://docs.ladybugdb.com/cypher/query-clauses/call)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Cypher, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Cypher that reads or modifies local Ladybug databases when the user runs it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
