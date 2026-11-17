## Description:

Query Polymarket prediction market odds and events via CLI, including market search, current prices, events by category, market details, tags, and orderbook depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceeyang](https://clawhub.ai/user/ceeyang)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve current Polymarket prediction-market odds, event listings, prices, tags, and orderbook data for questions about probabilities across sports, politics, crypto, business, technology, elections, and geopolitics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market search terms are sent to Polymarket public endpoints.

Mitigation: Avoid using the skill for private, sensitive, or unrelated probability questions.

Risk: Prediction-market odds can change quickly and may be unsuitable as the sole basis for decisions.

Mitigation: Treat returned odds as current market data and verify important conclusions against current sources before acting.

## Reference(s):

- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [ClawHub skill page](https://clawhub.ai/ceeyang/skills/polymarket-odds-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only lookup guidance and CLI output based on public Polymarket endpoints; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
