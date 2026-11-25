## Description:

Detects architectural clusters and coupling boundaries via community detection on the code graph

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify codebase module groupings, coupling boundaries, and possible refactoring targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Results may rely on directory and import summaries even though the skill describes graph-based community detection; one referenced path was not assessed.

Mitigation: Confirm graph data is available, review the evidence for clusters and coupling, and inspect unresolved local-path references before relying on refactoring suggestions.

## Reference(s):

- [Cartograph project page (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with community tables, Mermaid diagrams, and improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gauntlet graph data for graph-based clustering; otherwise falls back to directory and import analysis.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
