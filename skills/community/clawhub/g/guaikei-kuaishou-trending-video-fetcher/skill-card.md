## Description:

Fetches public Kuaishou video search results, creator posts, and video comments through GUAIKEI and returns structured JSON for trend, competitor, KOL, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, marketers, MCN operators, and analysts use this skill to collect public Kuaishou search, creator-post, and comment data for topic research, competitor monitoring, KOL filtering, and sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile URLs, video URLs, and the GUAIKEI API token are sent to guaikei.com.

Mitigation: Use only when that data sharing is acceptable, keep the token private, and rotate it if exposure is suspected.

Risk: Fetched public-data exports and logs may contain sensitive business research or user-derived public content.

Mitigation: Treat the logs/ directory as sensitive, limit access, and avoid committing or sharing generated logs.

Risk: The skill is limited to public Kuaishou data and can fail on private, deleted, restricted, or unavailable content.

Mitigation: Do not use it for private or logged-in data, and handle empty or error JSON statuses without inventing conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-trending-video-fetcher)
- [GUAIKEI API website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown responses with inline shell commands and structured JSON results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; fetched results may be saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, package.json, and changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
