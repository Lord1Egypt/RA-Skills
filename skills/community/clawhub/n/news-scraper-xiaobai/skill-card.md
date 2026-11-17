## Description:

News Scraper Xiaobai collects recent AI news from AIBase and helps agents organize items with categories, tags, links, summaries, and source metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahuishao](https://clawhub.ai/user/jiahuishao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect recent AI news from AIBase, return structured news records, and prepare concise categorized Markdown summaries for content aggregation or monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article URL handling could fetch unintended internal or external URLs.

Mitigation: Restrict article fetches to the intended AIBase HTTPS host and validate redirects before enabling the crawler in environments with private network access.

Risk: Fetched article text is untrusted web content that may influence downstream agent summaries.

Mitigation: Treat scraped article content as untrusted data and review generated summaries before reuse or publication.

Risk: Runtime dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies before deploying this skill in production or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiahuishao/skills/news-scraper-xiaobai)
- [AIBase news index](https://www.aibase.com/zh/news)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, Python snippets, and JSON news records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save a JSON file containing crawl time, total count, titles, URLs, publish times, sources, keywords, summaries, and article content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
