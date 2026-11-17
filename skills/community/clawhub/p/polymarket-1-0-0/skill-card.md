## Description:

Query Polymarket prediction markets - check odds, trending markets, search events, track prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leochan14](https://clawhub.ai/user/leochan14)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to query public Polymarket prediction-market data, including trending markets, keyword searches, category views, event lookups, odds, volume, and end dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and lookup requests are sent to Polymarket's public Gamma API.

Mitigation: Avoid submitting sensitive queries and review whether outbound requests to the Polymarket Gamma API are acceptable for the deployment environment.

Risk: The skill may install or use the Python requests package.

Mitigation: Review dependency installation policy and run the skill in an environment where Python package use is controlled.

Risk: The artifact does not explicitly declare outbound network scope.

Mitigation: Document and approve the required network destination before deployment.

## Reference(s):

- [Polymarket](https://polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket Documentation](https://docs.polymarket.com)
- [ClawHub Skill Page](https://clawhub.ai/leochan14/skills/polymarket-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted market summaries and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market data; results depend on Polymarket Gamma API availability and response content.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
