## Description:

Ontology provides a typed knowledge graph for structured agent memory, entity relationship management, constraints, and cross-skill state sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain local structured memory, create and query typed entities, model relationships and dependencies, and share state across composable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local ontology writes can retain sensitive or stale values in append-only graph files, including values that remain after logical deletes.

Mitigation: Do not store passwords, tokens, API keys, regulated data, or other secrets; use credential_ref or secret_ref indirection and review graph retention before sharing the workspace.

Risk: Validation may be advisory if mutation paths are used without enforcing schema checks before writes.

Mitigation: Run validation after schema changes and before using ontology data for decisions, and review mutation workflows that create, update, or relate entities.

Risk: Server security evidence marks the release suspicious because persistent writes are broader and less reliably validated than the documentation promises.

Mitigation: Review before installing, keep graph and schema paths scoped to the workspace, and inspect proposed file operations before execution.

## Reference(s):

- [Ontology Schema Reference](artifact/references/schema.md)
- [Query Reference](artifact/references/queries.md)
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/ontology-clawd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, Python, and shell command examples; CLI commands emit JSON or status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes append-only ontology records under memory/ontology by default and can create or merge schema files.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and skill.yaml; artifact _meta.json reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
