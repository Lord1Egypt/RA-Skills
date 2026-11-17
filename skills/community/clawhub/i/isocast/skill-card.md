## Description:

Isocast helps agents browse and optionally purchase weather-signal API data for Polymarket temperature markets, including city market URLs, bucket transitions, live odds, and optional Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use Isocast to inspect weather-market signal shapes, query city markets, and optionally purchase per-city signal bundles for Polymarket temperature-market workflows.

### Deployment Geography for Use:

Global, subject to local laws governing prediction markets, paid API purchases, and Telegram delivery.

## Known Risks and Mitigations:

Risk: The skill can guide an agent to contact an external API and use paid x402 signal routes.

Mitigation: Require explicit user approval before paid routes, Telegram delivery setup, or prediction-market use, and confirm the activity is legal in the user's jurisdiction.

Risk: Weather-market signals are informational and may be inaccurate or unsuitable for financial or betting decisions.

Mitigation: Present signals as informational only and avoid representing them as financial, betting, or outcome advice.

## Reference(s):

- [Isocast homepage](https://isocast.dev)
- [Isocast API docs](https://api.isocast.dev/llms.txt)
- [Isocast OpenAPI spec](https://api.isocast.dev/openapi.json)
- [ClawHub skill page](https://clawhub.ai/jcislo/skills/isocast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API examples, JSON endpoint shapes, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include x402 payment-flow guidance and Telegram delivery setup guidance when requested.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
