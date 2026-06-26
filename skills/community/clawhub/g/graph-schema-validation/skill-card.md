## Description: <br>
Validate knowledge graph schemas and data against defined ontology, RDF/OWL, or property graph schema constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to validate RDF/OWL and property graph schemas, check graph data before ingestion or deployment, and review violations with suggested corrections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested remediation queries or fixes could change graph records if applied directly to a live database. <br>
Mitigation: Review suggested fixes, test them in a staging environment, and back up graph data before applying changes. <br>
Risk: Validation results depend on the completeness and correctness of the schema rules supplied by the user. <br>
Mitigation: Review ontology, SHACL, property graph, and cardinality rules for domain coverage before relying on conformance status. <br>


## Reference(s): <br>
- [Graph Schema Validation skill page](https://clawhub.ai/fisa712/graph-schema-validation) <br>
- [Validation Patterns](references/validation-patterns.md) <br>
- [Graph Validation Examples](examples/example-validations.md) <br>
- [Schema Validator Script](scripts/schema_validator.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with code examples and validation report structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include detected violations, suggested corrections, conformance status, and example validation logic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
