## Description:

AI-powered ETF portfolio analysis for comparing signals across asset classes for allocation decisions, free and without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredxyt](https://clawhub.ai/user/fredxyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch public MoltStreet ETF signal data and compare portfolio allocation themes across equities, bonds, commodities, international funds, and thematic ETFs. It supports portfolio discussion and diversification review, not personalized financial advice or automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat AI-generated market signals as personalized financial, tax, retirement, or trading advice.

Mitigation: Present the signals as informational inputs only and recommend independent review before making investment decisions.

Risk: ETF tickers requested by the user may be sent to MoltStreet's public API.

Mitigation: Disclose the API use and avoid sending sensitive portfolio details beyond the tickers needed for the requested analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fredxyt/skills/moltstreet-portfolio)
- [MoltStreet](https://moltstreet.com)
- [MoltStreet skill documentation](https://moltstreet.com/skill.md)
- [MoltStreet API base](https://moltstreet.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with inline shell commands and summarized API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public MoltStreet API responses; no credentials, persistence, asset trading, or code installation.]

## Skill Version(s):

1.0.1 (source: server release evidence, manifest.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
