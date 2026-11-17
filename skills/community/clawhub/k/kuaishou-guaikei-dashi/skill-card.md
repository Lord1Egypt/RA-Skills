## Description:

Fetches public Kuaishou videos, creator posts, and comments through Guaikei APIs, returning structured JSON for content research, competitor monitoring, KOL discovery, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, MCN operators, and analysts use this skill to search public Kuaishou videos by keyword, inspect public creator posts, and collect public video comments for trend research and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, URLs, and the Guaikei API token are sent to the third-party guaikei.com service.

Mitigation: Use the skill only when that data sharing is acceptable, keep the token scoped and rotated according to the service provider's guidance, and avoid submitting sensitive private queries.

Risk: Returned public data and query context may be saved as local JSON logs.

Mitigation: Review and delete local log files when queries, returned comments, or analysis outputs are sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/kuaishou-guaikei-dashi)
- [Guaikei Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Structured JSON results with optional Markdown guidance and local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save query results under a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
