## Description:

Monitors VC investor activity and deal signals on Twitter using apidojo's Tweet scraper, returning investor handles, firms, thesis signals, recent activity, and deal flow indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, co-investors, and startup ecosystem analysts use this skill to monitor VC investor Twitter/X activity for investment thesis signals, sector interest, funding announcements, and deal-flow indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter search terms and retrieved results are sent through Apify/API Dojo services.

Mitigation: Confirm this data flow is acceptable before installation and avoid submitting confidential fundraising strategy or sensitive research queries.

Risk: Apify tokens can be exposed through URL query strings, shared logs, or committed environment files.

Mitigation: Use a dedicated least-privilege Apify token, keep tokens in environment variables or a local .env file, and exclude secrets from source control and shared logs.

Risk: Saved CSV or JSON outputs may contain sensitive market research or social media data.

Mitigation: Treat exported datasets as sensitive research records and apply appropriate access controls, retention limits, and review before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/monitoring-vc-investor-activity-on-twitter)
- [API Dojo Publisher Profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, API examples, result tables, and optional CSV or JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save retrieved results as CSV or JSON and can summarize classified investor activity with relevance scores.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
