## Description:

Build or refresh the CGIS code graph for this repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaebee](https://clawhub.ai/user/zaebee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or refresh a local CGIS semantic graph so agent tools can answer structural questions about a repository. It is intended for Python and TypeScript repository analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local graph.db can expose an index of private project structure.

Mitigation: Run ingestion only on code intended to be indexed and keep graph.db out of version control.

Risk: Selecting the wrong or overly broad source root can slow ingestion and pollute the graph with irrelevant files.

Mitigation: Prefer the repository src or package root and exclude node_modules, virtual environments, build outputs, and .git.

Risk: The graph becomes stale after substantial repository changes.

Mitigation: Rerun ingestion after major edits before relying on CGIS structural answers.

## Reference(s):

- [Server-resolved source provenance](https://github.com/zaebee/codegraph-brain/tree/main/plugin/skills/ingest)
- [ClawHub skill page](https://clawhub.ai/zaebee/skills/ingest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown status summary with repository graph metrics and follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports ingested file, node, and edge counts, unresolved edge share, unsupported repository languages, and graph.db maintenance guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
