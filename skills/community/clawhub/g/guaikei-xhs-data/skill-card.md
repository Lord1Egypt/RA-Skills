## Description:

小红书数据 helps agents search public Xiaohongshu notes, retrieve note details and comments, and collect public creator posts as structured data for content, market, competitor, KOL, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, market researchers, analysts, and social-media operators use this skill to retrieve public Xiaohongshu data for topic discovery, competitor monitoring, KOL screening, trend research, and comment analysis. Agents can route user requests to keyword search, note detail, creator post, or comment retrieval commands and then summarize the returned structured data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a third-party Guaikei API token and request data to guaikei.com, and the current code places the token in URL query parameters.

Mitigation: Install only when third-party API use is approved, treat GUAIKEI_API_TOKEN as sensitive, avoid sharing command traces that include request URLs, and rotate the token if exposure is suspected.

Risk: Search terms, Xiaohongshu profile URLs, comments, and returned public-data results may be written to the local logs directory.

Mitigation: Avoid sensitive queries when possible and review, restrict, or clear local logs after use according to the workspace data-handling policy.

Risk: The skill depends on a third-party public-data retrieval service, so API availability, authorization, or rate limits can affect results.

Mitigation: Handle empty or error status values as non-authoritative, retry later for transient failures, and verify important outputs before using them in reports or decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-data)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON data, Guidance]

**Output Format:** [JSON command output with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return status, error_code, message, request, skill_metadata, and results fields; successful runs also save local result logs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
