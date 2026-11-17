## Description:

Manages a persistent Obsidian-backed LLM wiki by initializing projects, ingesting source material into Markdown pages, answering wiki-based queries, and linting wiki health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to turn notes, papers, articles, and meeting records into an Obsidian wiki that preserves sources, cross-links concepts, records contradictions, and supports later queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages persistent Obsidian wiki files and may summarize or log sensitive material if used on a broad or sensitive vault area.

Mitigation: Use a dedicated project folder and avoid pointing the workflow at vault areas containing material that should not be summarized or logged.

Risk: Generated wiki updates can introduce inaccurate summaries, broken links, or unresolved contradictions in project knowledge.

Mitigation: Review planned ingest changes before writing, keep raw source files read-only, preserve contradictory claims with source notes, and run lint checks before relying on the wiki.

## Reference(s):

- [LLM Wiki concept by Andrej Karpathy](https://x.com/karpathy/status/1793562750870294638)
- [Ingest workflow reference](references/ingest-logic.md)
- [Scenario templates reference](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Conversational guidance and Markdown wiki files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Obsidian vault and the /obsidian skill; raw source files are documented as read-only.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
