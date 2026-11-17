## Description:

Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zy66677](https://clawhub.ai/user/zy66677)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to collect multi-source technology, finance, open-source, product, and social-trend news, then turn selected items into concise Chinese newsletter-style reports with source links and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep-fetch mode retrieves untrusted article URLs and page content through outbound web requests.

Mitigation: Run the skill in a sandboxed environment without access to private services or cloud metadata endpoints, and review fetched content before relying on it.

Risk: The skill saves generated news reports as local timestamped Markdown files.

Mitigation: Use a controlled workspace for report output and review saved files before sharing or importing them into other workflows.

Risk: Dependency and install-source pinning are not established by the provided evidence.

Mitigation: Pin Python dependencies and the skill install source before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zy66677/skills/news-aggregator-skill-0-1-0)
- [Publisher profile](https://clawhub.ai/user/zy66677)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown reports, JSON arrays from fetch_news.py, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save timestamped Markdown reports under reports/; deep-fetch mode adds article content fields capped to 3000 characters per item.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
