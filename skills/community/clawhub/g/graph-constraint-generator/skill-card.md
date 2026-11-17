## Description:

Generate structural, semantic, and property constraints for knowledge graph schemas including RDF/OWL ontologies and property graph models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to convert knowledge graph schema definitions into integrity constraints for RDF/OWL ontologies and Neo4j property graph models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SHACL shapes or Cypher statements may be incomplete or unsuitable for a specific production graph schema.

Mitigation: Review and test generated constraints against representative data before applying them to a real graph database.

Risk: Constraint templates may enforce overly broad, overly strict, or incorrect data-governance rules if the input schema is incomplete.

Mitigation: Validate generated constraints with domain owners and adjust cardinality, uniqueness, and required-property rules before deployment.

## Reference(s):

- [Constraint Generation Patterns](references/constraint-patterns.md)
- [Constraint Generation Examples](examples/example-constraints.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/graph-constraint-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown containing constraint summaries, Cypher statements, SHACL shapes, and RDF/OWL triples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated constraints should be reviewed and tested before use with production graph data or live databases.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
