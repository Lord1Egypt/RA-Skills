## Description:

Collects public Kuaishou data by searching videos by keyword, retrieving creator posts, and fetching video comments as structured JSON for content research, competitor monitoring, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, market researchers, data analysts, and agent developers use this skill to retrieve public Kuaishou search results, creator post lists, and comment data for content planning, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou search terms, creator URLs, video URLs, and API token-authenticated requests are sent to guaikei.com.

Mitigation: Install and run the skill only when this data sharing is acceptable; avoid submitting sensitive or unauthorized targets.

Risk: Query results, comments, or result data may remain in generated local logs.

Mitigation: Review or delete the generated logs directory when result data should not remain in the workspace.

Risk: The skill is limited to public Kuaishou data and can return empty or error results for private, deleted, unavailable, or unsupported content.

Mitigation: Use it only for public data collection and handle non-success statuses without fabricating missing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-creator-finder)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Guidance]

**Output Format:** [Structured JSON results with concise Markdown status and error summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save result logs in the workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
