## Description:

This skill produces structured A-share market broadcasts and market-sentiment recaps using public Investoday market data, including breadth, index performance, topical news, and session-stage interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate concise A-share market broadcasts for morning, midday, intraday, after-close, or general market-status questions. The skill helps summarize market breadth, major index movement, active themes, and follow-up signals without presenting the result as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic Chinese market-status questions may activate the skill and fetch current public market data.

Mitigation: Use clear invocation and review whether live market commentary is appropriate for the user request before relying on the output.

Risk: The broadcast is time-sensitive and may become stale as market prices, breadth, and news change.

Mitigation: Treat generated summaries as point-in-time commentary and refresh data before making decisions or sharing externally.

Risk: Users could mistake market commentary for personalized investment advice.

Mitigation: Preserve the skill's risk notice that outputs are based on real-time market and public information, are for reference only, and do not constitute investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-stock-market-broadcast)
- [Publisher profile](https://clawhub.ai/user/kenneth-bro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown market broadcast with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are time-sensitive commentary based on current public market data and should not be treated as investment advice.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
