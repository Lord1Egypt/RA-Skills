## Description:

Collects public Kuaishou content by searching videos, listing creator posts, and fetching video comments through Guaikei, returning structured JSON for content research, competitor monitoring, KOL discovery, comment review, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, market researchers, and analysts use this skill to collect public Kuaishou search results, creator post lists, and video comments for content research, competitor monitoring, KOL discovery, comment insight, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile or video URLs, limits, and GUAIKEI_API_TOKEN are sent to the Guaikei API.

Mitigation: Install and run only when this third-party data sharing is acceptable, and provide a scoped token through the environment.

Risk: Returned public comments and analysis data are saved locally under logs/.

Mitigation: Keep logs/ out of source control and delete saved outputs when they are no longer needed.

Risk: The skill is limited to public Kuaishou data and may return empty or error responses for deleted, private, unavailable, or rate-limited content.

Mitigation: Check the JSON status and error_code fields before using results in analysis or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-public-content-collector)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON with status, request metadata, skill metadata, and results; brief text may summarize successful results or explain errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful outputs are also saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog; artifact SKILL metadata lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
