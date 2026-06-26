## Description: <br>
Nova Memory helps agents store, retrieve, tag, analyze, and reflect on local workspace memories with entity support and local semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catplus-eric](https://clawhub.ai/user/catplus-eric) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace agents use this skill to persist selected local memories, retrieve them by semantic similarity or tag, manage entity facts, inspect a memory graph, and generate reflection or analytics summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected workspace information, tags, entities, and analytics data are persisted locally on disk. <br>
Mitigation: Avoid storing secrets or regulated personal data, keep the storage directory access-controlled, and periodically review or delete stale memory files. <br>
Risk: Broad trigger words or optional exports can cause more workspace context to be captured or copied into shared files than intended. <br>
Mitigation: Use explicit memory commands, review generated reflections before sharing, and avoid exporting sensitive memory summaries to shared documents. <br>


## Reference(s): <br>
- [Nova Memory on ClawHub](https://clawhub.ai/catplus-eric/nova-memory) <br>
- [Publisher profile](https://clawhub.ai/user/catplus-eric) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with Python API examples, CLI commands, JSON-like memory and graph data, and local analytics reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reference locally persisted memory records, tags, entities, graph relationships, and SQLite-backed analytics generated from the configured workspace storage directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
