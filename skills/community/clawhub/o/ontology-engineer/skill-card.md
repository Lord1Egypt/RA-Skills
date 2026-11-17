## Description:

Extract candidate ontology models from enterprise business systems and build or maintain local knowledge graphs from file systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li2092](https://clawhub.ai/user/li2092)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ontology engineers, and data consultants use this skill to extract candidate business ontologies from SQL DDL, Word, and Excel data dictionaries, or to build local knowledge graphs from approved file-system scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file-system indexing may capture personal, client, or partner data paths and extracted metadata.

Mitigation: Run only on specifically approved directories, start with dry-run and custom output paths, and avoid sensitive data unless authorization is clear.

Risk: Generated graph files may persist conversation facts, file paths, and extracted metadata.

Mitigation: Review graph.jsonl before syncing, committing, or sharing outputs, and keep generated files in a controlled local workspace.

Risk: Local scripts process Office, PDF, text, and structured files across large directory trees.

Mitigation: Use a sandboxed environment with pinned dependencies and confirm the Step 1.5 analysis scope before semantic analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li2092/skills/ontology-engineer)
- [Value scenarios](references/value-scenarios.md)
- [Analysis rules](references/analysis-rules.md)
- [Knowledge graph workflow](references/knowledge-graph-workflow.md)
- [Supported formats and dependencies](references/formats-and-deps.md)
- [Ontology modeling decision guide](references/modeling-decisions.md)
- [Relation ontology](references/relation-ontology.md)
- [Ontology evolution](references/ontology-evolution.md)
- [Constraints and inference](references/constraints-and-inference.md)
- [Quality self-check and error detection](references/quality-checks.md)
- [Script operations](references/script-operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, JSONL, YAML, and shell command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ontology.json and review.md for database extraction, or graph.jsonl and schema.yaml for file-system knowledge graphs.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
