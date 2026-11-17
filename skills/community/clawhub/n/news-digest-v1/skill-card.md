## Description:

Automatically scrapes Chinese news sources, filters and deduplicates articles, and generates daily summaries with source attribution and original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zigu-creator](https://clawhub.ai/user/zigu-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up a local Chinese news monitoring workflow that fetches news, filters low-relevance content, optionally summarizes with an LLM, and produces a daily digest for review or distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad network requests to configured news sites and custom article links.

Mitigation: Run it only with reviewed monitor_websites entries and trusted article sources before using the full pipeline.

Risk: The LLM stage can reuse an OpenClaw API key from local configuration when dedicated NEWS_DIGEST_LLM credentials are not set.

Mitigation: Set dedicated, limited NEWS_DIGEST_LLM_API_KEY and NEWS_DIGEST_LLM_BASE_URL values, or remove the OpenClaw config fallback before execution.

Risk: The skill writes a local SQLite database plus digest files in the workspace and Desktop.

Mitigation: Run it in a workspace where these writes are expected, and review generated digest content before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zigu-creator/skills/news-digest-v1)
- [Publisher profile](https://clawhub.ai/user/zigu-creator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text digest files with source titles, summaries, dates, and original links; setup guidance includes Markdown with bash and SQL snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .news-digest-out.md in the workspace and a timestamped Chinese text digest on Desktop; optional LLM summarization uses configured API credentials.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter and ClawHub release evidence, released 2026-06-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
