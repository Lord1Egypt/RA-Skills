## Description:

Validate knowledge graph schemas and data against defined ontology, RDF/OWL, or property graph schema constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to validate RDF/OWL and property graph schemas before ingestion, deployment, or migration. It helps identify missing properties, duplicate identifiers, invalid relationships, cardinality problems, and graph integrity issues, then produces reports and correction suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Cypher, SHACL, or correction suggestions could alter constraints or data if applied without review.

Mitigation: Review generated validation logic and fixes before running them against production graph databases or authoritative datasets.

Risk: Validation reports can flag issues that require domain judgment, such as whether an orphan node should be connected, removed, or retained.

Mitigation: Confirm reported violations with schema owners or data stewards before making destructive changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fisa712/skills/graph-schema-validation)
- [Graph Schema Validation Patterns](references/validation-patterns.md)
- [Graph Validation Examples](examples/example-validations.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with validation reports, Cypher or SHACL snippets, Python code examples, and suggested corrections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conformance status, violation counts, severity labels, affected node identifiers, and recommended fixes.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
