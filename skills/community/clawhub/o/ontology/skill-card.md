## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oswalpalash](https://clawhub.ai/user/oswalpalash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain a typed local knowledge graph for people, projects, tasks, events, documents, and related objects. It supports entity and relation CRUD, graph traversal, schema constraints, validation, and shared state across composable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores durable local knowledge graph data that may include sensitive workspace context. <br>
Mitigation: Control what agents are allowed to remember and periodically inspect memory/ontology/graph.jsonl and memory/ontology/schema.yaml. <br>
Risk: Passwords, tokens, or raw secrets could be placed into ontology records if a user or agent ignores the documented credential pattern. <br>
Mitigation: Do not store raw secrets; store references to a separate secret store and validate schemas that forbid secret-like credential properties. <br>
Risk: Updates and deletes are append-only, so prior values can remain in graph history. <br>
Mitigation: Avoid recording information that must be erased from local history, and review the append-only graph file before sharing or retaining it. <br>


## Reference(s): <br>
- [Ontology Schema Reference](artifact/references/schema.md) <br>
- [Query Reference](artifact/references/queries.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/oswalpalash/ontology) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local workspace files under memory/ontology, including graph.jsonl and schema.yaml.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
