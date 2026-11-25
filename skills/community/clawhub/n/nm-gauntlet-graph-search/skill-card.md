## Description:

Searches the code knowledge graph by function, class, or type using FTS5 full-text search

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find functions, classes, and types in a built code knowledge graph. They can search by name or qualified path, review matching locations and relevance, and open a result for further inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because it could not resolve several local path references.

Mitigation: Review unresolved references and the skill requirements before installation if additional assurance is needed.

Risk: A missing or stale code graph can prevent useful search results.

Mitigation: Build or refresh the graph before searching, and check its status before interpreting zero matches.

## Reference(s):

- [Gauntlet plugin documentation](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-gauntlet-graph-search)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown list or table of matching code entities, with qualified names, file paths, line numbers, and relevance scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 20 matches by default; optional filters can limit results to functions or classes.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
