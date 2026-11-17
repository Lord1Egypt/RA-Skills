## Description:

Analyzes public-company valuation and financial statements through a Chinese noodle-shop-owner lens, normalizing each company to a market value of 100 to compare book value, TTM profit or loss, and ROE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formyreason](https://clawhub.ai/user/formyreason)

### License/Terms of Use:

MIT-0

## Use Case:

External users analyzing listed companies use this Chinese-first skill to compare valuation, profitability, and balance-sheet strength with a consistent 100-value framework. It is intended for financial analysis and education, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial outputs can be misleading if public source data is stale, incomplete, or copied across inconsistent reporting periods.

Mitigation: Verify the source data, reporting period, currency, and accounting basis before relying on the analysis.

Risk: The skill can make strong comparative valuation judgments that may be mistaken for personalized investment advice.

Mitigation: Treat outputs as valuation education and require human review before making investment decisions.

Risk: Missing PE, PB, ROE, market-cap, or profit fields can invalidate the normalized comparison.

Mitigation: Follow the documented stop rule: report available fields and missing data instead of producing final comparisons.

## Reference(s):

- [Reference manual](artifact/reference.md)
- [Output examples](artifact/examples.md)
- [ClawHub skill page](https://clawhub.ai/formyreason/skills/noodles-shop-owner)
- [Publisher profile](https://clawhub.ai/user/formyreason)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with tables, calculations, and optional inline shell commands for local validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first financial-analysis style; requires current public financial data and stops when required fields are missing.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
