## Description:

Fetch and aggregate OpenClaw-related trends, news, tutorials, videos, and community discussions from YouTube, GitHub, X/Twitter, Reddit, Hacker News, and general web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andremashukov](https://clawhub.ai/user/andremashukov)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to collect recent OpenClaw-related content, deduplicate results, and produce a concise trend summary with source links and dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound web requests to third-party services while searching for OpenClaw content.

Mitigation: Install and run it only when external web requests to YouTube, GitHub, DuckDuckGo-backed web search, X/Twitter, Reddit, and Hacker News are acceptable.

Risk: The artifact includes an embedded YouTube API key that should be treated as exposed.

Mitigation: Remove the embedded key before deployment and require a user-provided YouTube API key through an environment variable or protected secret store.

Risk: The documented cron example can create scheduled background checks.

Mitigation: Add the cron entry only when scheduled daily trend checks are intentional and approved.

## Reference(s):

- [OpenClaw Trends on ClawHub](https://clawhub.ai/andremashukov/skills/openclaw-trends)
- [YouTube Data API v3 Search Endpoint](https://www.googleapis.com/youtube/v3/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON trend summaries with source, title, description, URL, and date fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron setup guidance for scheduled daily checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
