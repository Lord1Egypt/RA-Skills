## Description:

Kuai Shou Trend Insights retrieves public Kuaishou video search results, creator post lists, and video comments as structured JSON for trend research, competitor monitoring, KOL screening, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, analysts, and developers use this skill to collect public Kuaishou search, creator-post, and comment datasets for trend discovery, competitor monitoring, KOL screening, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required GUAIKEI_API_TOKEN may have account or billing value.

Mitigation: Store the token only in the execution environment, verify presence without printing it, and rotate it if it has already appeared in logs or terminal output.

Risk: Search terms, Kuaishou URLs, request parameters, and returned datasets are sent to Guaikei.

Mitigation: Use the skill only for queries and public data that are approved for that third-party service.

Risk: Successful runs save fetched datasets under the local logs/ directory.

Mitigation: Review, protect, or delete local logs according to the sensitivity and retention requirements of the collected data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/kuai-shou-trend-insights)
- [Guaikei API Token and Data Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON data, Guidance]

**Output Format:** [Markdown guidance with Node.js shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful command results include status, request metadata, skill metadata, and result data; successful runs also save returned datasets under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
