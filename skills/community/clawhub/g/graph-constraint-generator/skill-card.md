## Description: <br>
Generate structural, semantic, and property constraints for knowledge graph schemas including RDF/OWL ontologies and property graph models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and graph engineers use this skill to turn knowledge graph schema definitions, entity models, relationship types, property requirements, and integrity rules into database and semantic validation constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Cypher, SHACL, or index and constraint statements can change database schema behavior or affect validation outcomes. <br>
Mitigation: Review generated constraints in a development or staging environment before applying them to production graph data. <br>


## Reference(s): <br>
- [Constraint Generation Patterns](references/constraint-patterns.md) <br>
- [Constraint Generation Examples](examples/example-constraints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/graph-constraint-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Cypher, SHACL, RDF/OWL, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated constraint statements and validation queries should be reviewed before applying them to a live graph database or validation pipeline.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
