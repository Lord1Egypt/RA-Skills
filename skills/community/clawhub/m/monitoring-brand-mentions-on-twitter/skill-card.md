## Description:

Monitors and aggregates brand mentions on Twitter/X using apidojo's Tweet and Search scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External brand managers, PR teams, community managers, and reputation analysts use this skill to collect public Twitter/X mentions, summarize sentiment, and identify high-engagement praise or complaints for a brand, product, or keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed if they are passed in query parameters, shell history, logs, or saved examples.

Mitigation: Use scoped secrets or authorization headers where available, keep APIFY_TOKEN in the environment, and avoid logging commands that include tokens.

Risk: The customMapFunction input can send arbitrary JavaScript to the actor.

Mitigation: Use customMapFunction only with fully trusted code and review the transformation before execution.

Risk: Tweet exports and search terms may contain sensitive public-post metadata or internal monitoring priorities.

Mitigation: Limit searches to necessary terms and save CSV or JSON exports only in approved locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-brand-mentions-on-twitter)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables and optional shell/API command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tweet excerpts, author handles, engagement metrics, timestamps, sentiment groups, key themes, and optional CSV or JSON exports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
