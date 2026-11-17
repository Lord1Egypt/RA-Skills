## Description:

Typed knowledge graph for structured agent memory, entity and relation management, constraint validation, planning, and shared workspace state across skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep a local, typed memory graph for people, projects, tasks, events, documents, notes, credentials, and relationships. It supports creating, querying, linking, updating, deleting, and validating ontology records through local files and CLI examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a local persistent knowledge graph that may contain sensitive personal, project, or workspace information.

Mitigation: Do not store passwords, API keys, tokens, or other secrets in ontology properties, and review memory/ontology/graph.jsonl before sharing, syncing, or backing up the workspace.

Risk: Broad memory triggers can lead to unintended additions or changes in shared local workspace memory.

Mitigation: Confirm the intended entity, relation, and target graph before writes, and inspect the append-only graph history when reviewing changes.

Risk: Validation is a manual check rather than an enforced safety boundary.

Mitigation: Run validation as a review aid, but do not rely on it as the only control for data quality, policy enforcement, or sensitive-data handling.

## Reference(s):

- [Ontology Schema Reference](references/schema.md)
- [Query Reference](references/queries.md)
- [ClawHub skill page](https://clawhub.ai/wuliyuan2026/skills/ontology-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, YAML schema snippets, and Python API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local workspace files under memory/ontology when the ontology CLI is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
