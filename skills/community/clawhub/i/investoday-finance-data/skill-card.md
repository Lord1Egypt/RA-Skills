## Description:

Retrieves structured Chinese-market financial data for stocks, funds, indices, companies, research, and macroeconomic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial researchers use this skill to retrieve and compare structured data on Chinese equities, funds, indices, company financials, disclosures, research, sectors, and macroeconomic indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command can enable ongoing software and skill updates.

Mitigation: Use `investoday-api init --no-auto-update` unless continuing updates are intended; inspect update status and disable updates if the CLI is already initialized.

Risk: Query parameters are disclosed to InvestToday and may contain confidential research text.

Mitigation: Avoid including confidential research text in queries.

Risk: Quarterly and trailing-twelve-month figures can be confused when interpreting results.

Mitigation: Check the reporting-period labels before relying on financial figures.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kenneth-bro/skills/investoday-finance-data)
- [English API reference index](artifact/docs/references-index.en.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured financial data with concise Markdown summaries; may include CLI commands and JSON request bodies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on endpoint, time range, and data availability.]

## Skill Version(s):

1.8.99 (source: SKILL.md frontmatter; ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
