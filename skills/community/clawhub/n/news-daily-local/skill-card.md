## Description:

Fetches top news from domestic, international, technology, and AI RSS feeds and sends the digest to a Feishu group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morrison230](https://clawhub.ai/user/morrison230)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to collect daily news from configured RSS feeds, format the results as Feishu card messages, and send them manually or on a schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script disables HTTPS certificate verification while fetching RSS feeds and posting to a Feishu webhook.

Mitigation: Restore normal HTTPS certificate verification before deployment and rotate the Feishu webhook if this version has run on an untrusted network.

Risk: One RSS source uses plaintext HTTP, which can expose the digest pipeline to network tampering.

Mitigation: Replace or remove plaintext HTTP feeds and prefer HTTPS RSS sources.

Risk: A webhook token stored in a local config file may be readable by other users or processes.

Mitigation: Prefer the NEWS_DAILY_WEBHOOK environment variable or restrict permissions on any config file containing the webhook.

Risk: Scheduled execution can repeatedly post unreviewed external feed content to a Feishu group.

Mitigation: Review configured feeds and categories before enabling scheduled runs.

## Reference(s):

- [News Daily Local on ClawHub](https://clawhub.ai/morrison230/skills/news-daily-local)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Feishu card JSON, console status text, and Markdown-formatted news links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu webhook and configurable RSS categories; can run manually or on a schedule.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
