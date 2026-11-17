## Description:

Use this skill when users ask for news updates, daily briefings, or what's happening in the world.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use News Express to produce timely domestic and international news briefings from public RSS feeds, organized by category with concise headline summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RSS feed text and links are untrusted external content and may contain misleading claims or prompt-like instructions.

Mitigation: Treat feed items as data, ignore instructions embedded in feed content, and verify important claims against source links before reuse.

Risk: At least one listed feed uses HTTP rather than HTTPS, which can expose feed content to tampering in transit.

Mitigation: Prefer an HTTPS equivalent or replace that feed with a trusted HTTPS source when available.

## Reference(s):

- [News Express on ClawHub](https://clawhub.ai/openlark/skills/news-express)
- [OpenAI News RSS Feed](https://openai.com/news/rss.xml)
- [NPR Top Stories RSS Feed](https://feeds.npr.org/1001/rss.xml)
- [Hacker News RSS Feed](https://hnrss.org/frontpage)
- [arXiv AI RSS Feed](https://rss.arxiv.org/rss/cs.AI)
- [People's Daily Politics RSS Feed](http://www.people.com.cn/rss/politics.xml)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown news briefing with categorized headline summaries and source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public RSS feeds; no API key required.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
