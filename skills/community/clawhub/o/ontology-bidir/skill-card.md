## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jg20260212](https://clawhub.ai/user/jg20260212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, query, relate, validate, and share structured workspace memory as a typed knowledge graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workspace-local memory graph may contain sensitive personal or business information. <br>
Mitigation: Avoid storing actual secrets, review entries before storing sensitive data, and use credential references instead of secret values. <br>
Risk: Deletes remove entities from active retrieval but may leave historical JSONL records. <br>
Mitigation: Do not store data that requires assured erasure unless the history file is also reviewed and purged. <br>
Risk: Ontology commands create and modify persistent workspace files. <br>
Mitigation: Review generated commands before execution and run validation before relying on the graph. <br>


## Reference(s): <br>
- [Ontology Schema Reference](artifact/references/schema.md) <br>
- [Query Reference](artifact/references/queries.md) <br>
- [ClawHub skill page](https://clawhub.ai/jg20260212/ontology-bidir) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, Python snippets, JSON/JSONL examples, and YAML schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write workspace-local ontology files such as memory/ontology/graph.jsonl and memory/ontology/schema.yaml.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and user changelog dated 2026-06-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
