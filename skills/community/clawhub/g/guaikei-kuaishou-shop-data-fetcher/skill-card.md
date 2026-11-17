## Description:

Fetches public Kuaishou data for video search, creator post retrieval, and video comment extraction, returning structured results for analysis and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content creators, MCN teams, and analysts use this skill to collect public Kuaishou search results, creator posts, and video comments for topic research, competitor monitoring, KOL screening, sentiment review, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords or URLs and the GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Install and run the skill only when that data transfer is acceptable for the user, project, and organization.

Risk: Saved logs may retain scraped public data, creator identifiers, sensitive research topics, or business analysis.

Mitigation: Delete or protect local logs according to the sensitivity and retention requirements of the work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-shop-data-fetcher)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON with concise Markdown summaries and command-line invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save fetched results in local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog; SKILL.md metadata lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
