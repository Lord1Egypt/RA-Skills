## Description:

Build, maintain, query, and lint a persistent markdown knowledge wiki that sits between raw sources and final answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teki-ai](https://clawhub.ai/user/teki-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to build and maintain markdown or Obsidian-friendly wikis from notes, articles, transcripts, reports, and research, then query or lint those wikis over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change a user-directed markdown wiki during ingest, query, or lint workflows.

Mitigation: Ask for read-only answers when changes should not be saved, and review proposed edits to index.md, log.md, schema.md, and wiki pages before accepting them.

Risk: Incorrect synthesis, stale claims, or unresolved contradictions could become durable wiki content.

Mitigation: Keep source links and uncertainty notes visible, and use the lint workflow to find contradictions, stale claims, missing links, and duplicate pages.

## Reference(s):

- [Getting Started with an LLM Wiki](references/getting-started.md)
- [Wiki Patterns Reference](references/wiki-patterns.md)
- [Ingest Patterns](references/ingest-patterns.md)
- [Query Patterns](references/query-patterns.md)
- [Wiki Lint Checklist](references/lint-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with wiki pages, source summaries, analysis pages, index updates, log entries, answers, and lint reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist changes to user-directed wiki files such as index.md, log.md, schema.md, and topic, entity, concept, source, or analysis pages.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
