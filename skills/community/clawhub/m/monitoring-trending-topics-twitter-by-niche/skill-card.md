## Description:

Monitors trending topics and conversations in a specific niche on Twitter/X using apidojo's Twitter Search scraper, returning trend velocity, engagement signals, classifications, and top voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, PR teams, content strategists, and external analysts use this skill to monitor niche-specific Twitter/X conversations, identify emerging topics, and summarize trend velocity, engagement, and key voices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens may be exposed when using the REST fallback shown in the artifact.

Mitigation: Prefer the MCP path or a trusted runner that stores tokens in secure headers or a secret store, and avoid putting tokens in query strings.

Risk: Twitter/X search terms may reveal sensitive internal watchlists or strategy topics to Apify.

Mitigation: Use only approved search terms, avoid sensitive internal watchlists, and confirm that sending the selected terms to Apify is acceptable.

Risk: Unbounded tweet collection can increase cost, runtime, and data exposure.

Mitigation: Set a clear maxItems limit and apply filters that are appropriate for the monitoring task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-trending-topics-twitter-by-niche)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify Tweet Scraper actor](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, summaries, and optional shell commands for Apify execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV or JSON files when the user asks to save actor results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
