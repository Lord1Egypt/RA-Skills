## Description:

Turn structured data into shareable visual dashboards, reports, charts, and calendars. Publishes an A2UI JSON bundle to guiro.io and returns a short-lived share link that anyone can view; no login is required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chernojagne](https://clawhub.ai/user/chernojagne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Guiro to turn structured results such as metrics, tables, timelines, financial data, schedules, and progress tracking into browser-viewable dashboards, reports, charts, calendars, or status pages. The skill is suited for producing public, short-lived visual snapshots that users can share or print.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payload contents are sent to Guiro and the resulting no-login URL is public to anyone who has it until expiration.

Mitigation: Do not publish secrets, private customer data, confidential business records, or sensitive financial details unless the data is deliberately redacted and the user explicitly approves publication.

Risk: Passing the Guiro API key as a command-line argument may expose it through process logs or shell history.

Mitigation: Prefer GUIRO_API_KEY from the environment, avoid --api-key arguments when possible, and rotate any key that may have been exposed.

## Reference(s):

- [Guiro homepage](https://guiro.io)
- [Guiro API origin](https://api.guiro.io)
- [ClawHub skill page](https://clawhub.ai/chernojagne/skills/guiro)
- [Publisher profile](https://clawhub.ai/user/chernojagne)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and returned share-link JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUIRO_API_KEY and curl; successful creation returns a short-lived public Guiro URL and expiration timestamp.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
