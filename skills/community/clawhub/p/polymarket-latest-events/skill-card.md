## Description:

Fetch the latest events from Polymarket prediction market. Use when user asks about Polymarket events, prediction markets, trending bets, or wants to see what's new on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaplora](https://clawhub.ai/user/yaplora)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch and summarize active Polymarket events, trending prediction markets, odds, and event links from the public Gamma API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prediction market odds could be mistaken for financial advice.

Mitigation: Present odds as informational, include direct event links for context, and avoid investment or betting recommendations.

Risk: Broad trigger wording may cause outbound requests to Polymarket's public API for market or betting-related prompts.

Mitigation: Confirm intent when a request is ambiguous and disclose that results come from a third-party public API.

Risk: Results depend on third-party API freshness and availability.

Mitigation: State when data was fetched and treat missing or malformed API responses as unavailable data rather than filling gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yaplora/skills/polymarket-latest-events)
- [Polymarket Gamma events endpoint](https://gamma-api.polymarket.com/events?active=true&closed=false&limit=10&order=createdAt&ascending=false)
- [Polymarket Gamma tags endpoint](https://gamma-api.polymarket.com/tags?limit=100)
- [Polymarket Gamma sports endpoint](https://gamma-api.polymarket.com/sports)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown list with event titles, short descriptions or tags, odds, and event links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make outbound requests to Polymarket's public Gamma API; no credentials are required.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
