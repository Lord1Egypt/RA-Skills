## Description: <br>
Generate a structured knowledge graph ontology or schema from unstructured or semi-structured text sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge graph engineers use this skill to turn domain descriptions, technical documentation, and example data into initial ontology or property-graph schemas with entities, relationships, properties, and constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain text supplied to the skill may be echoed or transformed in generated schema output. <br>
Mitigation: Review sensitive input handling before use and avoid providing confidential text unless the deployment environment is approved for that data. <br>
Risk: Heuristic extraction can produce incomplete entities, ambiguous relationships, or misleading property assignments. <br>
Mitigation: Have a domain expert review generated schemas and validate relationship direction, constraints, and terminology before using them in production graph systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/kg-schema-from-text) <br>
- [Entity & Relationship Extraction Patterns](references/extraction-patterns.md) <br>
- [Schema Generation Examples](examples/example-schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with schema examples, JSON-like schema structures, Cypher snippets, and RDF/Turtle snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are draft graph schemas derived from supplied text and should be reviewed for domain accuracy before implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
