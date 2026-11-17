## Description:

Searches the code knowledge graph by function, class, or type using FTS5 full-text search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find functions, classes, and types in a code knowledge graph by name or qualified path. The graph must be built and current for search results to be meaningful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan could not resolve four local path references, so their contents were not included in the reviewed skill content.

Mitigation: Review the referenced scripts in the installed plugin before running them.

Risk: A missing or stale code graph can make search unavailable or results unreliable.

Mitigation: Check that the graph exists and is current; build or refresh it with the graph-build skill when needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-gauntlet-graph-search)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown search results with qualified names, file paths, line numbers, and relevance scores.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a search term and optional entity-kind filter; the documented default result limit is 20. Offers to read the top result's source file.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
