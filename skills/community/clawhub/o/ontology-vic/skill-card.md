## Description:

Typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to maintain a typed local knowledge graph for structured memory, entity CRUD, relation management, graph traversal, and cross-skill state sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist shared workspace state in local ontology files.

Mitigation: Use it only when shared agent memory is intended, review proposed writes, and keep append-only changes auditable.

Risk: Ontology entries may include secrets or sensitive personal data if agents are allowed to store them directly.

Mitigation: Store only references to credentials or sensitive records, and avoid writing secrets, tokens, passwords, or unnecessary personal data into the graph.

Risk: Documented CLI workflows depend on a local ontology.py script that is not included in this artifact.

Mitigation: Review the local script before running the documented commands and require confirmation before commands that write to memory/ontology.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/ontology-vic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline YAML, JSONL, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on local append-only ontology files under memory/ontology and optional schema validation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
