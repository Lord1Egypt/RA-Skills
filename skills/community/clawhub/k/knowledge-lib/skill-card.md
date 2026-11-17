## Description:

Personal knowledge wiki manager that organizes notes into structured Markdown pages with concept pages, summaries, and cross-references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual knowledge-base users use this skill to save links or files into a local Markdown wiki, summarize sources into concept and summary pages, query existing knowledge with citations, and run health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write outside its stated knowledge folder when category, slug, or raw-file paths are untrusted.

Mitigation: Use only trusted category, slug, and raw-file inputs until containment validation is added; review generated file paths before execution.

Risk: URL ingestion is presented as offline behavior but normal link ingestion expects the agent to fetch web content.

Mitigation: Treat link ingestion as a network operation and apply the same review, source trust, and data handling controls used for fetched content.

Risk: Persistent logs, summaries, and analyses can retain sensitive material in the knowledge base.

Mitigation: Avoid ingesting sensitive content unless persistent local storage is acceptable for the workspace.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, text answers, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes raw documents, summaries, concept pages, analyses, indexes, and operation logs under the configured knowledge base directory.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
