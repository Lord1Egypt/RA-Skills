## Description:

Portfolio Copilot creates conversational Paradex portfolio briefings that combine account summary, positions, balances, transfers, market data, and funding into natural-language status and P&L answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sv](https://clawhub.ai/user/sv)

### License/Terms of Use:

MIT-0

## Use Case:

External Paradex users use this skill to ask for concise portfolio status, position, P&L, balance, transfer, funding, daily recap, and morning briefing answers. It helps summarize read-only account and market data without presenting the output as trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad portfolio-status prompts could cause unintended disclosure of Paradex account data.

Mitigation: Use explicit Paradex account context and confirm the user intended a portfolio briefing before summarizing account details.

Risk: Portfolio values, prices, and positions are point-in-time financial data that can change continuously.

Mitigation: Present summaries as snapshots and avoid treating them as trading advice.

Risk: Realized P&L and time-period estimates may be incomplete because closed-trade realized P&L is not directly available from the current data sources.

Mitigation: Label period P&L as approximate and direct users to the Paradex UI for complete trade history when needed.

## Reference(s):

- [Briefing Format Templates](references/briefing-formats.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language Markdown briefings with short prose and tables when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account snapshots; realized P&L and period estimates may be incomplete or approximate.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
