## Description:

Aggregates recent AI and investing news from configured RSS feeds and Bing News RSS, then guides an agent to produce a concise Chinese news brief with deduplication, ranking, and impact analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huntingfishdude](https://clawhub.ai/user/huntingfishdude)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect recent AI, technology, and market news and turn it into a Chinese daily brief. It is suited for news-monitoring workflows that need source links, rough importance ranking, and short impact analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes external network requests to news feeds and Bing News RSS.

Mitigation: Install and run it only in environments where outbound news requests are acceptable, and review configured sources before use.

Risk: Python package installation may pull dependencies from the configured package index.

Mitigation: Use a virtual environment and pin or review feedparser and requests before deployment.

Risk: Fetched news titles, snippets, and article text are untrusted external content.

Mitigation: Treat fetched content as untrusted input and review generated summaries before relying on them.

Risk: The README still mentions duckduckgo-search even though server security guidance identifies that instruction as stale.

Mitigation: Use the current SKILL.md and script dependency guidance, and remove the stale duckduckgo-search instruction during release cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huntingfishdude/skills/news-scout)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [News source configuration](artifact/resources/news_sources.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown brief with source links; helper script emits JSON news data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The instructed final brief contains 10 items split across investing, global AI, and China AI sections.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
