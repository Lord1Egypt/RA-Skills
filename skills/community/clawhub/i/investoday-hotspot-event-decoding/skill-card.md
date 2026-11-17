## Description:

Decodes market hotspot, theme, sector, and industry events by extracting recent core events, logic chains, opportunity and risk directions, and follow-up validation points from Investoday financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to understand recent theme, sector, or industry catalysts and produce a structured hotspot event decoding report. It is intended for theme-level research and observation, not single-stock news analysis or investment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-theme analysis may be mistaken for investment advice.

Mitigation: Keep outputs informational, avoid single-stock recommendations, and preserve the risk notice that conclusions do not constitute investment advice.

Risk: Recent market news and research sentiment can become stale or uncertain.

Mitigation: Include the analysis date and only list news or research titles that were actually used in the report.

Risk: The skill depends on the Investoday finance data skill for public market data.

Mitigation: Confirm that the finance data dependency is available and use a more specific workflow for single-stock news or macro-only commentary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenneth-bro/skills/investoday-hotspot-event-decoding)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an analysis date, core events, event decoding, opportunity and risk directions, follow-up observation points, cited news or research titles, and a risk notice that the output is informational and not investment advice.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
