## Description:

Generate declarative mapping rules that transform structured data sources into graph triples or nodes using a domain-specific mapping language similar to R2RML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to generate reusable mapping specifications that transform structured sources such as databases, CSV files, JSON, and APIs into knowledge graph nodes, relationships, triples, or property graph mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DSL or R2RML can include unescaped schema names, predicates, URI templates, endpoints, or credentials supplied by a user.

Mitigation: Validate and escape mapping fields before execution, prefer structured JSON or YAML serializers, and review generated mappings for unintended sources or transformations.

Risk: Mappings generated from untrusted source definitions may reference sensitive data sources or unsafe transformation behavior.

Mitigation: Use least-privilege execution environments and manually inspect source definitions, transformations, and credentials before running the mappings on real data.

## Reference(s):

- [Mapping DSL Design Patterns](references/mapping-patterns.md)
- [Mapping DSL Examples](examples/example-mappings.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/mapping-dsl-builder)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, YAML, JSON, Turtle/R2RML, and custom mapping DSL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable mapping configuration examples that should be reviewed before use with real data sources.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
