## Description: <br>
Design property graph schemas for knowledge graph systems using Neo4j-style node labels, relationships, and properties based on domain descriptions or developer requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data modelers use this skill to convert domain descriptions, system documentation, ER diagrams, relational schemas, API schemas, or business rules into Neo4j-style property graph schemas with labels, relationships, properties, constraints, indexes, and Cypher templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Cypher or schema recommendations may be inappropriate for a live Neo4j database if applied without review. <br>
Mitigation: Review generated Cypher, constraints, and indexes before applying them to production data stores. <br>
Risk: Example schemas or tests may expose real personal data if users paste sensitive domain examples into the workflow. <br>
Mitigation: Use synthetic or sanitized examples unless privacy controls and approvals are in place. <br>


## Reference(s): <br>
- [Property Graph Schema Design Patterns](references/schema-patterns.md) <br>
- [Property Graph Schema Examples](examples/example-schemas.md) <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/property-graph-schema-designer) <br>
- [Publisher profile](https://clawhub.ai/user/fisa712) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Cypher and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include schema summaries, node and relationship definitions, constraints, index recommendations, and Cypher implementation templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
