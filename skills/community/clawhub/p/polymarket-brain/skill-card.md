## Description:

Automates geopolitical and macroeconomic news analysis, matches expert insights to Polymarket odds, and posts actionable trade recommendations to Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimaschand29](https://clawhub.ai/user/dimaschand29)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to route CNBC geopolitical and macroeconomic news through expert analysis, compare expert probabilities with Polymarket odds, and prepare Discord-ready market commentary. The output is financial commentary and should not be treated as trade execution or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships live Discord webhooks and can send local analysis to a fixed external Discord channel without clear user control.

Mitigation: Revoke and replace bundled webhooks, configure destinations through environment variables or a secret manager, and run a dry-run or content preview before enabling outbound delivery.

Risk: Generated Discord output contains market commentary that could be mistaken for financial advice.

Mitigation: Treat all output as commentary only, review recommendations manually, and keep the not-financial-advice disclaimer visible in downstream messages.

Risk: Clearing article history in production can cause repeated analysis and repeated outbound posts.

Mitigation: Avoid clearing history outside test runs and back up history files before any maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dimaschand29/skills/polymarket-brain)
- [Polymarket API](https://gamma-api.polymarket.com/events)
- [Workflow reference](artifact/references/workflow.md)
- [Discord output format](artifact/references/discord-format.md)
- [Configuration reference](artifact/references/config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown Discord messages, JSON analysis artifacts, and command-line workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts may be sent to Discord webhooks; users should preview content and configure their own secrets before running.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
