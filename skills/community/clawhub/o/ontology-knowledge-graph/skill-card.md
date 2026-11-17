## Description:

Ontology 知识图谱 provides a typed knowledge graph for structured agent memory, including entity CRUD, relation queries, schema validation, and memory-file sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, validate, query, and link structured memory entities such as people, projects, tasks, events, documents, and skills. It can also serve as a backup memory layer when primary memory search returns incomplete or inaccurate results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auto-sync feature can permanently add hard-coded person, organization, and ownership records to the local memory graph.

Mitigation: Remove or disable those defaults before enabling sync, run dry-run previews first, and review pending graph writes before allowing persistent updates.

Risk: ID-collision or validation behavior could produce misleading structured memory.

Mitigation: Validate the graph after changes, keep append-only history for review, and fix collision handling before using synced graph data as a trusted memory source.

Risk: Broad activation or scheduled sync can write stale or unintended memory extracted from local notes.

Mitigation: Narrow activation and write rules, limit the sync window, and review scheduled sync configuration before deployment.

## Reference(s):

- [Ontology Schema Reference](artifact/references/schema.md)
- [Query Reference](artifact/references/queries.md)
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/ontology-knowledge-graph)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python examples; CLI commands emit JSON or text and can append JSONL ontology records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local ontology graph and schema files under memory/ontology when commands are executed.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
