## Description: <br>
Generate declarative mapping rules that transform structured data sources into graph triples or nodes using a domain-specific mapping language similar to R2RML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to define reusable mappings from databases, CSV, JSON, and APIs into knowledge graph entities, properties, relationships, triples, and related mapping specifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated mappings may include connection strings, bearer tokens, API keys, or database credentials supplied by the user. <br>
Mitigation: Use placeholders or secret references in mapping files and avoid embedding live credentials in generated DSL, YAML, JSON, R2RML, examples, or documentation. <br>
Risk: Incorrect source schema, identifier, relationship, or transformation assumptions can produce misleading graph mappings. <br>
Mitigation: Review generated mappings against the source schema and test them with representative sample data before deployment. <br>


## Reference(s): <br>
- [Mapping DSL Builder on ClawHub](https://clawhub.ai/fisa712/mapping-dsl-builder) <br>
- [Mapping DSL Design Patterns](references/mapping-patterns.md) <br>
- [Mapping DSL Examples](examples/example-mappings.md) <br>
- [OpenClaw Homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated mapping specifications in custom DSL, R2RML, YAML, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source schema mappings, entity definitions, property mappings, relationship mappings, URI templates, and transformation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
