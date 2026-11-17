## Description:

NewsLatest helps agents fetch and present hot-news ranking data from multiple public platforms through the NewsLatest API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violetlength](https://clawhub.ai/user/violetlength)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to retrieve current trending topics from one specified platform or aggregate results across multiple supported public platforms. It is suited for hot-news, trending-topic, and platform-specific ranking requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests for hot-news rankings are sent to the disclosed external API at newslatest-server.up.railway.app.

Mitigation: Avoid including private or sensitive details in requests and invoke the skill with explicit platform or source names.

Risk: Frequent requests may create unnecessary load or stale-cache confusion.

Mitigation: Respect the artifact guidance to wait at least 30 seconds between requests and prefer cached data unless a refresh is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/violetlength/skills/newslatest)
- [NewsLatest API base URL](https://newslatest-server.up.railway.app)
- [Single-source news endpoint](https://newslatest-server.up.railway.app/news/{source})
- [Combined news endpoint example](https://newslatest-server.up.railway.app/news/combined?sources=baidu,weibo,zhihu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted news rankings with titles, heat values, descriptions, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API response interpretation and fallback text for missing descriptions, heat values, or mobile URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
