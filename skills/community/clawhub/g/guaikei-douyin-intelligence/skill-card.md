## Description:

Guaikei Douyin Intelligence helps agents search public Douyin content, fetch creator posts, retrieve video comments, and query real-time hot trends for competitor analysis, content planning, and public-opinion monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketing teams use this skill to collect structured public Douyin search results, creator posts, comments, and hot-list data for short-video research, competitor monitoring, campaign planning, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search terms, target profile URLs, video URLs, and API tokens to guaikei.com.

Mitigation: Use it only for data flows approved by the deploying organization, avoid confidential research unless that external service use is acceptable, and rotate the API token if exposure is suspected.

Risk: Security evidence reports that token-error behavior can expose onboarding or contact text despite the skill's stated neutral-error policy.

Mitigation: Review runtime error output before deployment and require neutral authentication failures in any approved release.

Risk: Fetched results are stored locally in log files.

Mitigation: Treat generated logs as potentially sensitive research data and apply retention, access-control, and deletion policies appropriate for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-intelligence)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [JSON Schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command stdout is intended to be parseable JSON; runtime logs and prompts are written separately, and individual data requests are capped at 10,000 results.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog, and constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
