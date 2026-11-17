## Description:

Fetches public Kuaishou videos, creator posts, and comments through the Guaikei API and returns structured JSON for content research, competitor monitoring, KOL screening, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, marketers, content creators, and MCN teams use this skill to search public Kuaishou videos by keyword, retrieve public creator posts, and collect comments for downstream analysis and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile URLs, video URLs, and the GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only with approved public inputs, manage the token as a secret, and confirm that sending these requests to the third-party API is acceptable for the deployment.

Risk: Successful runs save returned posts and comments to local JSON log files.

Mitigation: Store, retain, and delete logs according to the user's data-handling policy, especially when results include user-generated comments.

Risk: Returned posts and comments are public user-generated data that may be incomplete, unavailable, or unsuitable for unrestricted redistribution.

Mitigation: Treat results as source data for review and analysis, verify important conclusions before use, and follow platform terms and applicable privacy rules.

## Reference(s):

- [Guaikei API access and support](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-public-data-fetcher)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON with status, error_code, request, skill_metadata, and results fields, plus concise human-readable guidance when inputs or API calls fail.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful runs are written to local JSON files under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
