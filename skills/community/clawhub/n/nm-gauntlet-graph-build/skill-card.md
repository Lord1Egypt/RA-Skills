## Description:

Builds or updates the code knowledge graph via tree-sitter AST and SQLite

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build or update a structural knowledge graph for a codebase before searching it or analyzing change impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial; some `.gauntlet/graph.db` references were unavailable for review.

Mitigation: Before installing, confirm that `.gauntlet/graph.db` matches your intended use and review the skill’s behavior in your environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-gauntlet-graph-build)
- [Project page](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands, a JSON build report, and a SQLite graph database]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Builds or updates `.gauntlet/graph.db` in the selected codebase; uses an incremental update when a graph already exists.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
