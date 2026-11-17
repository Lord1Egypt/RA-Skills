## Description:

Fetches public Kuaishou data by searching videos by keyword, listing creator posts, and retrieving video comments, returning structured JSON for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, creators, marketers, MCNs, and analysts use this skill to collect public Kuaishou search results, creator post lists, and video comments for content research, competitor monitoring, KOL screening, trend analysis, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou search terms, profile/video URLs, and the GUAIKEI_API_TOKEN are sent to the guaikei.com API.

Mitigation: Use the skill only when that external API transfer is acceptable, keep the token scoped and protected, and rotate it if exposure is suspected.

Risk: Generated logs may retain sensitive research targets, queries, returned comments, or competitive analysis data.

Mitigation: Store logs in an access-controlled location and delete or redact them when the retained data is no longer needed.

Risk: The skill is limited to public Kuaishou data and can return empty or error JSON when inputs are invalid, unavailable, or rate limited.

Mitigation: Check the returned status and error code before drawing conclusions, and avoid using it for private, hidden, or login-required data.

## Reference(s):

- [Guaikei service portal](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-open-data-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command results may also be saved to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
