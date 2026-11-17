## Description:

Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[administratorfung](https://clawhub.ai/user/administratorfung)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch multi-source news, filter by source or keyword, deep-fetch article content when requested, and produce concise Chinese news briefings or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep-fetch mode can make outbound requests to article URLs discovered from public feeds.

Mitigation: Run the skill in an isolated environment with restricted network egress and avoid --deep on untrusted or overly broad result sets.

Risk: Fetched content and generated reports may contain inaccurate, stale, or misleading news summaries.

Mitigation: Review generated reports before relying on or redistributing them, especially for finance, market, or breaking-news content.

Risk: Reports are automatically written to the reports/ directory.

Mitigation: Review saved reports for sensitive or unwanted content and manage the reports/ directory according to local data-retention expectations.

Risk: Dependencies are not version-pinned in requirements.txt.

Mitigation: Pin and review dependencies before installation in production or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/administratorfung/skills/news-aggregator-skill-3)
- [Publisher profile](https://clawhub.ai/user/administratorfung)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports in Simplified Chinese, with JSON arrays returned by fetch_news.py when invoked directly]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under reports/ with timestamped filenames.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
