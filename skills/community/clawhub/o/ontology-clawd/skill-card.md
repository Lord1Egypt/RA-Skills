## Description: <br>
Ontology provides a typed knowledge graph for structured agent memory, entity relationship management, constraint validation, and cross-skill state sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, query, link, and validate typed entities such as people, projects, tasks, events, and documents. It supports persistent local graph memory and shared state across composable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may capture sensitive or outdated information. <br>
Mitigation: Avoid storing passwords, tokens, and highly sensitive content, and review memory/ontology periodically. <br>
Risk: Unreviewed graph mutations could create, update, link, or delete records unexpectedly. <br>
Mitigation: Ask the agent to confirm before mutating ontology records and run validation after schema or graph changes. <br>
Risk: Incorrect constraints or stale relations can lead to misleading query results. <br>
Mitigation: Use the validate command and inspect task, relation, and schema changes before relying on them for planning. <br>


## Reference(s): <br>
- [Ontology Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/ontology-clawd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON, YAML, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can create or update local JSONL graph files and YAML schema files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
