## Description:

Fundamental equity analysis and peer ranking using a structured scoring playbook for business quality, balance-sheet safety, cash flow, valuation, sector adjustments, and confidence modifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to analyze one or more public stock tickers, compare peers, rank candidates, and produce an educational fundamentals-based verdict with confidence and risk context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis outputs may be mistaken for investment advice or used without independent verification.

Mitigation: Treat outputs as educational analysis, verify cited financial data before acting, and consult qualified professionals for investment decisions.

Risk: Public financial data can be stale, conflicting, incomplete, or paywalled.

Mitigation: Use the required data quality scorecard, cite sources, mark unavailable metrics as NA, and lower confidence when freshness, coverage, or source quality is weak.

Risk: Open-ended browsing could drift beyond relevant public finance sources.

Mitigation: Restrict retrieval to ticker-relevant filings, issuer materials, reputable financial aggregators, and relevant financial news as described by the skill security scope.

## Reference(s):

- [Mars Stock Analysis on ClawHub](https://clawhub.ai/mars82311111/skills/mars-stock-analysis)
- [Fundamental Stock Analysis Playbook](references/playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ticker resolution, scored verdicts, confidence level, data quality notes, risk discussion, recent news links, and source attribution; user-facing output excludes machine-readable JSON blocks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
