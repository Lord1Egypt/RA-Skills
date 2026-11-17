## Description:

News Market aggregates Chinese A-share market news from fixed RSS feeds and web sources, with include and exclude keyword filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mc82465](https://clawhub.ai/user/mc82465)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and filter current Chinese A-share market, technology, securities, and official-channel news, then summarize titles, sources, links, and article excerpts for readers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched article text and links come from third-party RSS and news sites and may be inaccurate, stale, or misleading.

Mitigation: Treat retrieved content as untrusted and verify market-moving claims against authoritative sources before acting on them.

Risk: Some configured feeds use HTTP or third-party mirrors, which can create content-integrity risk.

Mitigation: Prefer an updated version that replaces HTTP feeds with HTTPS and clearly labels remote content sources.

Risk: RSS feeds and scraped pages can fail or change format, causing incomplete results.

Mitigation: Use the returned results as partial coverage and corroborate important news through primary publisher or official-channel pages.

## Reference(s):

- [News Market ClawHub page](https://clawhub.ai/mc82465/skills/news-market)
- [RSSHub official instance](https://rsshub.app)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text news lists or JSON arrays, often summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include article titles, sources, timestamps, links, summaries, and full RSS-provided text when requested.]

## Skill Version(s):

1.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
