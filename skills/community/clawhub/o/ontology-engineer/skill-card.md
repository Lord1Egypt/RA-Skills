## Description: <br>
Extracts candidate ontology models from enterprise schemas and data dictionaries, and builds local knowledge graphs from approved filesystem scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li2092](https://clawhub.ai/user/li2092) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and ontology practitioners use this skill to extract business concepts, relationships, and review artifacts from schemas, data dictionaries, and selected file collections. It supports local knowledge graph creation when the user confirms the scan scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly scan folders and derive sensitive data from local files. <br>
Mitigation: Use it only on folders intentionally selected and authorized by the user; prefer dry-run or custom output paths before full analysis. <br>
Risk: Generated graph and schema artifacts may persist sensitive derived information. <br>
Mitigation: Store outputs in a controlled local directory, review them before sharing, and avoid scanning shared, client, or private locations without authorization. <br>
Risk: Runtime conversation facts can become durable memory if passive writes are allowed. <br>
Mitigation: Require explicit user opt-in before saving chat-derived facts to persistent graph files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/li2092/ontology-engineer) <br>
- [Analysis Rules](references/analysis-rules.md) <br>
- [Knowledge Graph Workflow](references/knowledge-graph-workflow.md) <br>
- [Supported Formats and Dependencies](references/formats-and-deps.md) <br>
- [Ontology Modeling Decision Guide](references/modeling-decisions.md) <br>
- [Relation Ontology](references/relation-ontology.md) <br>
- [Constraints and Inference](references/constraints-and-inference.md) <br>
- [Ontology Evolution](references/ontology-evolution.md) <br>
- [Quality Self-Check and Error Detection](references/quality-checks.md) <br>
- [Script Operations](references/script-operations.md) <br>
- [Value Scenarios](references/value-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, YAML, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local files such as ontology.json, review.md, graph.jsonl, and schema.yaml] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local artifacts generated from user-selected inputs; review is expected before using extracted models or knowledge graphs.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
