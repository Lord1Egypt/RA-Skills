## Description:

Fetches public Kuaishou data by keyword, creator profile, or video URL and returns structured JSON for content research, competitor monitoring, KOL screening, comment analysis, and trend insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, MCN teams, analysts, and agents use this skill to collect public Kuaishou search results, creator posts, and video comments for downstream analysis and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou search terms, profile URLs, video URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only when that third-party API sharing is acceptable, and avoid submitting private, sensitive, or unauthorized data.

Risk: Fetched public data is saved locally in logs.

Mitigation: Review and delete local logs when retained public data is no longer needed.

Risk: The skill is limited to public Kuaishou data and may return empty or error responses for private, deleted, login-required, or unsupported content.

Mitigation: Check the returned status and error code before using results in analysis or reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-public-post-fetcher)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON returned from Node.js command-line scripts, with optional Markdown summaries or follow-up analysis from the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; fetched public data is saved locally under logs/ by the scripts.]

## Skill Version(s):

1.0.0 (source: server release, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
