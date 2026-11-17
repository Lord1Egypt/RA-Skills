## Description:

Design property graph schemas for knowledge graph systems using Neo4j-style node labels, relationships, and properties based on domain descriptions or developer requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn domain descriptions, ER diagrams, relational schemas, API schemas, and business rules into Neo4j-style property graph designs. It helps draft node labels, relationship types, properties, constraints, indexes, and Cypher templates for graph database projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Cypher, labels, property names, constraints, or indexes may be incorrect for the target graph database or domain model.

Mitigation: Review generated schema elements and Cypher before applying them in Neo4j or another property graph system.

Risk: Attacker-controlled schema names or domain inputs could lead to unsafe generated statements if used directly.

Mitigation: Validate and sanitize externally supplied labels, relationship types, property names, and identifiers before using helper-script output.

## Reference(s):

- [Property Graph Schema Design Patterns](references/schema-patterns.md)
- [Property Graph Schema Examples](examples/example-schemas.md)
- [SchemaBuilder helper script](scripts/schema_builder.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Cypher and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Cypher and schema recommendations are drafts for review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
