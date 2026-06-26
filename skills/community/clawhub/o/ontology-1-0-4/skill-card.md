## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenmyword](https://clawhub.ai/user/tenmyword) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, query, relate, and validate typed ontology entities for local agent memory and cross-skill state sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent local agent memory in workspace files. <br>
Mitigation: Install it only when persistent ontology memory is intended, and review proposed memory writes before accepting remembered or linked facts. <br>
Risk: Ontology records may include personal, secret-adjacent, or otherwise sensitive information if users place it in graph properties. <br>
Mitigation: Do not store secrets or highly sensitive personal data in the ontology graph; use secret references for credentials and review graph contents before sharing the workspace. <br>
Risk: Incorrect entity links or schema constraints can create misleading agent memory. <br>
Mitigation: Use the validation workflow and inspect relation changes when adding or merging schema and graph data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tenmyword/ontology-1-0-4) <br>
- [Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local workspace files under memory/ontology for graph and schema storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
