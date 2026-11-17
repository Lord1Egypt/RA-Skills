## Description:

Provides a typed knowledge graph for structured agent memory, entity CRUD, relation modeling, validation, and shared state across skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonydesign1999](https://clawhub.ai/user/tonydesign1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, query, update, link, and validate typed workspace knowledge as a local ontology graph. It supports shared memory patterns for tasks, projects, people, events, documents, notes, credentials by reference, and cross-skill state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent ontology files may retain sensitive or unwanted workspace memory.

Mitigation: Use only in workspaces where shared memory under memory/ontology is acceptable, and avoid storing secrets, tokens, passwords, or private personal data in graph records.

Risk: Graph mutations may store invalid data if validation is incomplete or not run before writing.

Mitigation: Limit use to explicit ontology read/write requests, review proposed mutations, define schema constraints, and run validation before relying on graph contents.

## Reference(s):

- [Ontology Schema Reference](references/schema.md)
- [Query Reference](references/queries.md)
- [ClawHub skill page](https://clawhub.ai/tonydesign1999/skills/ontology-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, YAML, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workspace files under memory/ontology when used.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
