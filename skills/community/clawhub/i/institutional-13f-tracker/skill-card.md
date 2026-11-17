## Description:

13F institutional ownership tracker: quarterly hedge fund and mutual fund holdings from SEC 13F filings, by ticker or by manager, with top institutional holders per stock, quarter-over-quarter buying and selling deltas, and activist investor positions across thousands of managers. Use for 13F filings, 13F holdings changes, hedge fund holdings, institutional ownership by ticker, who owns this stock, activist fund positions, and superinvestor portfolios. Read-only. No trading, no purchases, no write operations, no wallet access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and investors can use the skill to review institutional ownership, manager holdings, and quarter-over-quarter 13F changes. Its results provide informational context and are not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some local references in SKILL.md could not be resolved.

Mitigation: Check the unresolved references and review the skill before relying on it.

Risk: 13F data is quarterly and delayed, and dollar flows are estimates from quarter-end snapshots rather than reported trades.

Mitigation: State the reporting date, describe flows as estimates, and present results as informational context rather than real-time positions or advice.

Risk: API calls require an authentication key, which could be exposed if handled unsafely.

Mitigation: Keep SENTISENSE_API_KEY in the environment and send it in the request header; do not put it in a query string or user-facing output.

## Reference(s):

- [SentiSense API](https://app.sentisense.ai)
- [Institutional 13F Tracker on ClawHub](https://clawhub.ai/thesentitrader/skills/institutional-13f-tracker)
- [SentiSense](https://sentisense.ai)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational summaries of quarterly 13F snapshots; dollar flows are estimates, not reported trades or cash flows. No personalized investment advice or trading actions.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
