## Description:

Researches the last 30 days across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and web search, then synthesizes the results into a recent-evidence brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to gather and summarize recent social, community, market, GitHub, and web signals about a person, company, product, competitor, launch, or trend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and retrieved snippets may be sent through AISA-hosted services.

Mitigation: Use approved AISA credentials and avoid submitting sensitive or restricted topics unless that data sharing is acceptable.

Risk: GitHub API reads may use a configured GH_TOKEN or GITHUB_TOKEN.

Mitigation: Use least-privilege tokens and review local configuration files before enabling GitHub-backed searches.

Risk: Optional Xiaohongshu/local API and watchlist webhook paths can connect to logged-in services or outbound endpoints.

Mitigation: Enable those paths only when intended, verify local service configuration, and send webhooks only to endpoints you control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/last30days-aisa)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON research brief with provider runtime, query plan, ranked candidates, clusters, and items grouped by source when JSON is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally save Markdown or JSON artifacts when a save directory is provided.]

## Skill Version(s):

1.0.4 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
