## Description:

Detects architectural clusters and coupling boundaries via community detection on the code graph

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to identify architectural clusters, module boundaries, and coupling patterns in a codebase while exploring refactoring targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The graph-based workflow may not be available as described; fallback directory and import summaries may not provide graph-based community results, and a local tool reference is unresolved.

Mitigation: Confirm the gauntlet graph tool and graph data are available, and review fallback summaries before using results to guide refactoring.

## Reference(s):

- [Cartograph plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Mermaid diagram, Refactoring guidance]

**Output Format:** [Markdown with a community table, coupling warnings, a Mermaid flowchart, and improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Graph-based results require gauntlet graph data; otherwise the skill uses directory and import summaries.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
