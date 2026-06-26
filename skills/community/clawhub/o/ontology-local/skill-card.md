## Description: <br>
Ontology Local provides a typed local knowledge graph for creating, querying, linking, and validating structured agent memory across entities such as people, projects, tasks, events, and documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain a local typed memory graph, query relationships, and validate task, project, person, event, and document records that need to be shared across skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores structured memory in local workspace files, which may include sensitive personal, project, or operational details if users add them. <br>
Mitigation: Do not store passwords, tokens, or unnecessary private details; review the ontology files periodically and remove data that should not persist. <br>
Risk: The skill can create and update files under memory/ontology as part of normal use. <br>
Mitigation: Review proposed commands and file changes before relying on them, and keep backups for important workspace memory. <br>
Risk: Server release evidence and bundled metadata report different versions. <br>
Mitigation: Verify the publisher, release version, and artifact contents before installation or upgrade. <br>


## Reference(s): <br>
- [Ontology Local on ClawHub](https://clawhub.ai/wuliyuan2026/ontology-local) <br>
- [Ontology Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local workspace files under memory/ontology when the user runs the provided commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; bundled metadata reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
