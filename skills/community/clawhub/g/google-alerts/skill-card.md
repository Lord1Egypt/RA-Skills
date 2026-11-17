## Description:

Monitors user-configured Google Alerts RSS feeds for brand, product, industry, competitor, and market keywords and formats results for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and automation agents use this skill to fetch configured Google Alerts RSS results for keywords and turn them into concise monitoring output for brand, competitor, industry, and market tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Google Alerts feed ID is a user-specific identifier that can appear in environment variables, shell profiles, or logs.

Mitigation: Use only feed IDs you are comfortable exposing to the agent environment and avoid storing sensitive alert identifiers in shared profiles or logs.

Risk: The skill reads only configured Google Alerts RSS feeds, so results depend on the user-created alerts and are not a complete general web search.

Mitigation: Confirm that the configured alerts match the monitoring task and verify important findings against primary sources before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bgoodwinstudio/skills/google-alerts)
- [Google Alerts](https://www.google.com/alerts)
- [Setup guide](references/setup-guide.md)
- [Keyword definitions](references/keywords.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [JSON arrays from the search script and markdown-style formatted text cards from the formatter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, python3, and GOOGLE_ALERT_FEED_ID; reads configured Google Alerts RSS feeds.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
