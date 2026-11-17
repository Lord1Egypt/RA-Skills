## Description:

Collects structured public Kuaishou data by keyword search, creator posts, and video comments for trend, competitor, KOL, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketing analysts, MCN operators, and data analysts use this skill to fetch public Kuaishou search results, creator post lists, and video comments for downstream reporting and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile URLs, video URLs, requested limits, and GUAIKEI_API_TOKEN are sent to the Guaikei service.

Mitigation: Use the skill only when the user approves that data transfer, avoid sending sensitive research terms, and keep the API token scoped and protected.

Risk: Generated local JSON logs may contain business, competitor, or social-media research data.

Mitigation: Store logs in an approved location, restrict access, and delete them when they are no longer needed.

Risk: The skill depends on a third-party API service and may return rate-limit, token, timeout, or service-error responses.

Mitigation: Check returned status and error_code before analysis, reduce request limits or retry later for transient failures, and do not treat empty or error responses as factual results.

Risk: The skill is intended for public Kuaishou data and does not support private, hidden, or login-only content.

Mitigation: Reject requests for private or non-public data and use returned data only within applicable authorization and redistribution limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-rank-data-fetcher)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON data, files]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output includes status, error_code, request metadata, skill metadata, and results; successful runs may also save JSON logs locally.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
