## Description:

Fetches public Kuaishou videos, creator posts, and video comments through the Guaikei API for competitive research, content planning, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, MCN teams, and data analysts use this skill to retrieve public Kuaishou search results, creator post lists, and video comments for trend research, competitive monitoring, KOL screening, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile or video URLs, and requested result parameters are sent to guaikei.com with the configured API token.

Mitigation: Use the skill only when this third-party data flow is acceptable, and avoid sending sensitive research terms or URLs unless they are approved for that service.

Risk: Fetched research data may be written to the local logs directory.

Mitigation: Review, retain, or delete generated logs according to the workspace's data handling requirements.

Risk: The skill is limited to public Kuaishou data and may return empty or error results for private, deleted, unavailable, or rate-limited content.

Mitigation: Check the returned status and error_code fields before using the results in analysis or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-video-comment-fetcher)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON results from the invoked command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results include status, error_code, request metadata, execution metadata, and fetched public Kuaishou data when successful; task results may also be saved under a local logs directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog released 2026-08-29, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
