## Description: <br>
Ontology provides a typed knowledge graph for structured agent memory, entity relationships, validation constraints, and cross-skill state sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Ontology to create, query, link, and validate typed entities such as people, projects, tasks, events, and documents as persistent local memory for multi-step workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent local graph data that can contain sensitive personal, project, account, or workflow information. <br>
Mitigation: Avoid storing secrets or highly sensitive personal data, review memory/ontology/graph.jsonl periodically, and manually delete or purge ontology files when retained history must be removed. <br>
Risk: Append-only graph and schema updates may retain stale or incorrect facts after an entity changes. <br>
Mitigation: Use update, delete, validation, and periodic review workflows to keep the graph accurate before relying on it for planning or cross-skill state sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/ont-v1) <br>
- [Ontology Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON/YAML examples, and local JSONL/YAML graph files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory/ontology graph and schema files; graph data should be reviewed before use in decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
