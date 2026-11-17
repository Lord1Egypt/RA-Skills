## Description:

Ontology provides a typed knowledge graph for structured agent memory, entity CRUD, relation queries, constraint validation, graph-based planning, and cross-skill state sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenmyword](https://clawhub.ai/user/tenmyword)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain shared structured memory as typed entities and relations, then query, link, validate, and reuse that graph across planning and other skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist shared workspace memory that later agents may read or mutate.

Mitigation: Install it only in workspaces where shared memory is intended, and review ontology changes before relying on them.

Risk: The graph may contain sensitive personal data or secrets if agents store them directly.

Mitigation: Avoid storing secrets or sensitive personal data directly; use credential references or secret references instead.

Risk: Security evidence says validation promises are stronger than the current CLI enforcement before writes.

Mitigation: Run validation before relying on graph contents and treat validation results as a review gate for important workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenmyword/skills/ontology-1-0-4)
- [Ontology Schema Reference](artifact/references/schema.md)
- [Query Reference](artifact/references/queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON/YAML examples; CLI output is JSON or status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or mutate local workspace files under memory/ontology, including graph.jsonl and schema.yaml.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
