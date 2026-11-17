## Description:

Full-text search across structured Markdown documentation archives using SQLite FTS5 with BM25 ranking and source URL extraction for citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carev01](https://clawhub.ai/user/carev01)

### License/Terms of Use:


## Use Case:

Developers, researchers, and technical writers use this skill to index structured Markdown documentation archives, run full-text queries, retrieve matching articles, and cite source URLs during documentation research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results can expose snippets, file paths, source URLs, and optional full article content from indexed Markdown.

Mitigation: Index only documentation intended for agent access; avoid directories containing secrets or private notes, and use full-content output only when complete articles are needed.

Risk: Regex mode can behave poorly with untrusted or expensive patterns.

Mitigation: Prefer the indexed SQLite FTS5 search path for routine queries, and avoid regex mode with untrusted patterns.

## Reference(s):

- [Documentation Search Patterns](references/search-patterns.md)
- [ClawHub skill page](https://clawhub.ai/carev01/skills/md-docs-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI search results can be emitted as text, JSON, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires indexing documentation before search; optional full-content output may return complete article text.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
