## Description:

Builds or updates the code knowledge graph via tree-sitter AST and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can build or refresh a structural knowledge graph of a codebase before searching it or analyzing the impact of changes. The skill reports build results and suggests graph search or blast-radius analysis as next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or updates `.gauntlet/graph.db` in the selected codebase, and the security scan could not fully resolve references to that local path.

Mitigation: Review the target directory and confirm that creating or updating the graph database is intended before running the skill.

## Reference(s):

- [ClawHub graph-build release](https://clawhub.ai/athola/skills/nm-gauntlet-graph-build)
- [Related project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON build report with a concise Markdown summary and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes parsed file, node, edge, and duration counts when available.]

## Skill Version(s):

1.10.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
