## Description:

Generates Chinese-language industry research reports for a commodity or sector, covering price trends, drivers, supply chain context, major news, A-share company exposure, financial impact, turnover, and technical analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitertigerwilson](https://clawhub.ai/user/whitertigerwilson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare structured Chinese-language research on commodities, industries, and related China A-share companies. The skill is intended for research assistance and includes investment-risk disclaimers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial research outputs may be incomplete, stale, or mistaken for investment advice.

Mitigation: Treat outputs as research assistance only, retain the disclaimer, and verify company data against public filings and current market sources before relying on conclusions.

Risk: Public web and Chinese market-data services may return unavailable, delayed, or inconsistent data.

Mitigation: Cross-check prices with multiple sources as the skill directs, and review discrepancies before publishing a report.

Risk: Optional Python dependencies and market-data scripts may vary by local environment.

Mitigation: Use an isolated Python environment with reviewed and pinned dependencies before installing or running optional packages such as akshare.

## Reference(s):

- [Industry research reference manual](references/research_manual.md)
- [ClawHub skill page](https://clawhub.ai/whitertigerwilson/skills/industry-research-cn)
- [Eastmoney quote site](https://quote.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown research report with tables, cited source notes, and script-generated market metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a financial disclaimer and calls for cross-checking market prices across multiple public sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
