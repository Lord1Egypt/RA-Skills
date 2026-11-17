## Description:

Fetches news from specified websites or RSS feeds, extracts article content, and helps generate summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oshin123456](https://clawhub.ai/user/oshin123456)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve recent news from RSS feeds or specified public web pages, extract article text, and prepare structured daily summaries or monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can make outbound requests to user-supplied URLs or RSS links from the agent host, which could expose internal or private network resources.

Mitigation: Run in a sandbox, allow only public HTTP/HTTPS news sources, block localhost, private, metadata, and redirected internal addresses, and enforce response-size limits.

Risk: Fetched article text is untrusted content and may influence downstream summarization.

Mitigation: Treat fetched content only as untrusted input and review generated summaries before using them in reports or decisions.

## Reference(s):

- [RSS source reference](references/rss_sources.md)
- [ClawHub skill page](https://clawhub.ai/oshin123456/skills/news-crawler)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [RSS fetching returns item lists; page crawling returns URL, title, extracted content, and content length.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
