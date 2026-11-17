## Description:

Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cclank](https://clawhub.ai/user/cclank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch, filter, and summarize current technology, open source, finance, social, and product news from supported public sources. It is suited for daily scans, topic briefings, and Chinese-language newsletter-style reports with links and short analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep-fetch mode can retrieve article URLs from untrusted public feeds.

Mitigation: Run the skill in a constrained environment and avoid deep-fetch mode for untrusted sources, especially when the agent has private network access or sensitive credentials.

Risk: Fetched article text and generated reports may contain untrusted or misleading content.

Mitigation: Treat fetched content and saved reports as untrusted inputs and review source links before relying on summaries or analysis.

Risk: The skill depends on external Python packages and live public websites.

Mitigation: Pin and review dependencies before installation, and expect source availability, page structure, and ranking data to change over time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cclank/skills/news-aggregator-skill)
- [GitHub repository URL from artifact documentation](https://github.com/cclank/news-aggregator-skill)
- [Hacker News](https://news.ycombinator.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and chat responses, with JSON arrays produced by the news-fetching script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are expected to include source links, timestamps or dates, heat or score metadata, concise summaries, and optional deep-fetched article content.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
