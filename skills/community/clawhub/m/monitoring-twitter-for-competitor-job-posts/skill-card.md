## Description:

Monitors Twitter/X for competitor hiring announcements with Apify's apidojo Tweet scraper, then extracts roles, departments, dates, urgency signals, growth classifications, and scoring for competitive intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Competitive intelligence teams, recruiters, and investors use this skill to monitor competitor hiring signals on Twitter/X and summarize growth patterns by role, department, timing, urgency, and relevance score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented REST curl fallback can expose the user's Apify API token in URLs.

Mitigation: Prefer the MCP/client helper or Authorization headers, use a narrowly scoped Apify token, avoid copying tokens into URLs, and rotate the token if query-string commands were run in logged environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-twitter-for-competitor-job-posts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown table and summary, with optional JSON or CSV files when saved through the actor helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Apify token and produces results based on Twitter/X scraper output quality and query coverage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
