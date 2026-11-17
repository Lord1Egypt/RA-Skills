## Description:

Generate a structured knowledge graph ontology or schema from unstructured or semi-structured text sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft knowledge graph schemas from domain descriptions, technical documentation, example records, or structured data samples. It helps identify entities, relationships, properties, and target graph representations such as Property Graph or RDF/OWL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Cypher and RDF/Turtle may contain incorrect, misleading, or unsafe identifiers when source text is ambiguous or untrusted.

Mitigation: Review and validate generated entities, relationships, properties, and identifiers before running them against Neo4j or importing them into graph tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fisa712/skills/kg-schema-from-text)
- [Extraction patterns](references/extraction-patterns.md)
- [Example schemas](examples/example-schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with schema examples, plus optional Python-generated dictionaries, Cypher statements, and RDF/Turtle snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated graph schemas should be treated as drafts and reviewed before import or execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
