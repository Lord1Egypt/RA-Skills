## Description:

Typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, query, link, and validate typed entities for shared agent memory, task tracking, dependency analysis, and cross-skill state sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent ontology history can retain sensitive workspace data in JSONL records.

Mitigation: Use the skill only with data suitable for persistent local storage and avoid entering passwords, tokens, API keys, or other secrets.

Risk: Validation may not provide strict write-time enforcement for every documented constraint.

Mitigation: Run validation after changes and review proposed graph/schema updates before relying on them for automated decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/ont-v1)
- [Ontology schema reference](references/schema.md)
- [Ontology query reference](references/queries.md)
- [Legacy ClawHub skill homepage](https://clawhub.com/skills/ontology)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; CLI operations emit JSON or status text and write JSONL/YAML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local append-oriented ontology files under memory/ontology by default.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
