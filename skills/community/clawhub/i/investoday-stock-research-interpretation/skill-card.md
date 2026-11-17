## Description:

This skill helps agents interpret A-share single-stock research reports by identifying stock codes, using Investoday finance data, and summarizing institutional views, rating changes, core rationale, opportunities, risks, and consensus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance analysts use this skill to ask about recent institutional views, rating changes, sell-side logic, target-price context, and consensus for a single A-share stock. The skill produces an informational research-interpretation report and avoids buy/sell, position-sizing, target-price upside, or trading-timing advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad Chinese finance phrases about institutional views or research report interpretation.

Mitigation: Use it for single A-share stock research interpretation queries and route industry, sector, news, announcement, or single-message analysis to more specific skills.

Risk: Users may mistake institutional research interpretation for investment advice.

Mitigation: Keep outputs informational, include evidence coverage and data-window limits, and avoid buy/sell recommendations, position sizing, target-price upside calculations, or trading-timing advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-stock-research-interpretation)
- [Publisher profile](https://clawhub.ai/user/kenneth-bro)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research interpretation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes analysis date, Investoday data-source framing, recent research and rating windows, evidence coverage notes, opportunity and risk summaries, and follow-up validation signals.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
