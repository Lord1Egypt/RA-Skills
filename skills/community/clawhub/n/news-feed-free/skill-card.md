## Description:

新闻订阅 helps agents fetch recent headlines from major RSS sources such as BBC, Reuters, and AP, with options for source selection, keyword filtering, time windows, deduplication, and JSON or Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor news topics, collect recent RSS headlines, filter by source or keyword, and export briefings for analysis or follow-up writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell execution even though public RSS headline fetching may not require broad command access.

Mitigation: Review commands before execution, grant only the minimum tool access needed, and run the skill in a constrained environment.

Risk: The artifact suggests a generic API_KEY environment variable without clearly identifying the required service.

Mitigation: Do not set a generic API_KEY unless the publisher documents the service and scope; prefer scoped secrets with service-specific names.

Risk: Custom RSS URLs and export paths can introduce untrusted network targets or unintended file writes.

Mitigation: Prefer HTTPS feeds from trusted sources, validate custom RSS URLs, and restrict exports to an expected working directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-feed-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [BBC News RSS feed](http://feeds.bbci.co.uk/news/rss.xml)
- [Reuters Top News RSS feed](https://feeds.reuters.com/reuters/topNews)
- [Associated Press Top News RSS feed](https://feeds.apnews.com/rss/apf-topnews)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON news lists and briefings, with occasional shell command examples for export or environment setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include source labels, publication times, URLs, summaries, duplicate markers, and export files.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-08-25T14:22:01.571Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
