## Description:

Searches Kuaishou public data, retrieves creator posts, and fetches video comments as structured JSON for topic research, competitor monitoring, KOL screening, sentiment analysis, and trend insight workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, analysts, and agents use this skill to search Kuaishou videos, retrieve public creator posts, and collect public video comments for topic research, competitor monitoring, KOL screening, sentiment review, and trend reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GUAIKEI_API_TOKEN and sends it to the Guaikei API service for each request.

Mitigation: Use a narrowly scoped token, keep it in the environment, rotate it if exposed, and avoid printing or pasting it into terminals or chats.

Risk: Successful queries save full structured result files in the local logs/ directory.

Mitigation: Review, retain, or delete local result logs according to the user's data-handling policy after each workflow.

Risk: The skill calls a third-party API service with Kuaishou keywords, profile identifiers, video URLs, and query options.

Mitigation: Confirm that the target data is public and that sending those query details to Guaikei is acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-trend-insights)
- [Guaikei API token service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Files, Analysis]

**Output Format:** [JSON result objects with status, request metadata, skill metadata, and results; successful runs also write JSON result files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and Node.js 16.14.0+; routes keyword, creator profile/user ID, and video URL inputs to separate Kuaishou search, post, and comment commands.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md metadata, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
