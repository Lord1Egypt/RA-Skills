## Description:

Typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jg20260212](https://clawhub.ai/user/jg20260212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain a local typed knowledge graph for entities, relations, task dependencies, planning state, and cross-skill shared memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent shared workspace memory can retain sensitive, stale, or invalid ontology records.

Mitigation: Avoid storing secrets or highly sensitive personal data, and run validation before relying on persisted graph data.

Risk: Broad activation can cause routine agent workflows to create or update shared graph state.

Mitigation: Review intended ontology changes and keep append/merge history so prior definitions are not overwritten.

## Reference(s):

- [Ontology Schema Reference](references/schema.md)
- [Query Reference](references/queries.md)
- [ClawHub Skill Page](https://clawhub.ai/jg20260212/skills/ontology-bidir)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, JSON, JSONL, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local workspace ontology files, primarily memory/ontology/graph.jsonl and memory/ontology/schema.yaml.]

## Skill Version(s):

1.1.0 (source: server release metadata and user changelog, released 2026-06-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
