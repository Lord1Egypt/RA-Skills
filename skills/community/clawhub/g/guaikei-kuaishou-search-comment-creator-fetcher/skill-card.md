## Description:

This skill helps agents research public Kuaishou content by searching keywords, fetching creator posts, and retrieving video comments for structured analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content operators, brand researchers, and creators use this skill to collect public Kuaishou search results, creator videos, and video comments for topic research, competitor tracking, trend analysis, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Kuaishou search terms, profile or video URLs, request parameters, and the Guaikei API token to www.guaikei.com.

Mitigation: Confirm the user is comfortable with this third-party data transfer before running the skill, especially for sensitive research targets.

Risk: The skill writes fetched results to local log files that may contain sensitive research targets or comments.

Mitigation: Review, protect, or delete generated logs when the collected data should not remain on disk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-search-comment-creator-fetcher)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON responses with status, request metadata, skill metadata, and results, plus concise agent-facing guidance when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save fetched results to local logs.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog released 2026-08-29, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
