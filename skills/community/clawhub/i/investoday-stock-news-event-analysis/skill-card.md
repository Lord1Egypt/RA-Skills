## Description:

Analyzes recent A-share stock news and event signals using Investoday financial data, identifying stock codes and producing a structured news-event analysis report focused on sentiment, institutional validation, market response, catalysts, and risk messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to analyze recent A-share company news, announcements, research sentiment, ratings changes, and live market feedback. It produces a structured report that summarizes core events, directional event sentiment, institutional validation, market response, and follow-up signals without giving investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an INVESTODAY_API_KEY and live Investoday API access.

Mitigation: Configure the API key only in the intended runtime environment and review credential handling before deployment.

Risk: Broad trigger terms may route queries that are better suited to intraday price movement, single-news interpretation, or analyst-report workflows.

Mitigation: Review routing behavior and prefer the more specific related skill when the user asks about today's price move, a single news item, or institutional analyst views.

Risk: Finance outputs can be mistaken for investment recommendations.

Mitigation: Keep reports informational, preserve the skill's prohibition on buy or sell advice, and clearly state when evidence is insufficient or signals diverge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-stock-news-event-analysis)
- [Publisher profile](https://clawhub.ai/user/kenneth-bro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown stock news-event analysis report with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INVESTODAY_API_KEY and the investoday-finance-data skill; outputs are informational and must not include buy or sell advice, target-price upside calculations, position sizing, or short-term trading recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
