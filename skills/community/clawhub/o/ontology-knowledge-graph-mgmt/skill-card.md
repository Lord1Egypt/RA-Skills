## Description:

Guides agents through knowledge graph data completion, validation, repair, SQLite synchronization, vector search integration, and optional vector database setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain ontology-backed knowledge graph data, synchronize graph records into SQLite, and add vector search workflows for graph retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on external Python scripts that are not included with the skill and are not tied to a trusted source or integrity checks.

Mitigation: Install and run the graph scripts only from an authoritative repository or pinned release with checksums, and test them in an isolated project account before using real graph data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william202404/skills/ontology-knowledge-graph-mgmt)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes graph.jsonl record examples, SQLite synchronization commands, vector indexing commands, search commands, and optional vector database configuration choices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
