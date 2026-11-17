## Description:

Import CSV transactions with deduplication, calculate exact totals and budgets, and export ledgers. Use for Expense Tracker and Budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

External users can maintain a household expense ledger, import user-supplied CSV transaction exports, set category budgets, and review income, expenses, and refunds by date and currency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial records and earlier exports remain stored locally without encryption.

Mitigation: Use a private workspace, back up the ledger, and review imported records and exported reports.

## Reference(s):

- [Expense Tracker input contract](references/input.md)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-expense-tracker)

## Skill Output:

**Output Type(s):** [Text, CSV files, Markdown reports]

**Output Format:** [Text summaries, a CSV ledger, and a Markdown budget report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Currencies are reported separately; exports include file paths and SHA256 receipts.]

## Skill Version(s):

1.1.1 (source: frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
