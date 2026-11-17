## Description:

Monitors Instagram for brand mentions and tagged posts using apidojo's Instagram scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Brand managers, social listening teams, PR agencies, and community managers use this skill to collect public Instagram mentions, classify sentiment and mention type, and prepare brand health reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Instagram monitoring data to Apify and may involve personal data, regulated brands, competitors, or confidential campaigns.

Mitigation: Review the intended monitoring scope before installation, use approved Apify or vendor controls, limit exported fields, and define retention and deletion rules for saved CSV or JSON results.

Risk: The documented REST fallback places an API token in the request URL, which can expose credentials through logs or history.

Mitigation: Prefer the MCP or runner flow, or pass credentials through an authorization header or another approved secret-handling mechanism.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-instagram-brand-mentions)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/instagram-scraper](https://apify.com/apidojo/instagram-scraper)
- [Apify actor REST endpoint](https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Data files]

**Output Format:** [Markdown report with tables, inline shell commands, and optional CSV or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Instagram post URLs, captions, author handles, engagement counts, timestamps, mention types, sentiment summaries, and reach scoring.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
