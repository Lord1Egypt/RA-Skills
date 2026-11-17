## Description:

MoltStreet lets agents check AI market signals, read multi-analyst research, and track prediction accuracy for stocks, ETFs, and crypto through public API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredxyt](https://clawhub.ai/user/fredxyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and summarize third-party AI-generated market commentary, ticker-level signals, analyst consensus, prediction records, and paper-trading context. It supports market research and outlook questions, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MoltStreet responses are third-party, AI-generated financial commentary and may be incomplete, stale, or unsuitable for a user's circumstances.

Mitigation: Present the output as market research, not investment advice, and encourage independent verification before any trading decision.

Risk: Ticker, portfolio, or trading-interest queries can reveal user interests to the MoltStreet service.

Mitigation: Avoid sending sensitive portfolio details unless the user is comfortable sharing those query terms with the service.

## Reference(s):

- [MoltStreet ClawHub Skill Listing](https://clawhub.ai/fredxyt/skills/moltstreet)
- [MoltStreet Homepage](https://moltstreet.com)
- [MoltStreet Skill Documentation](https://moltstreet.com/skill.md)
- [MoltStreet API Base URL](https://moltstreet.com/api/v1)
- [MoltStreet Disclaimer](https://moltstreet.com/disclaimer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline curl commands and JSON or text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public MoltStreet API endpoints with no API key; requires curl for command examples.]

## Skill Version(s):

1.8.2 (source: server release metadata, manifest.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
