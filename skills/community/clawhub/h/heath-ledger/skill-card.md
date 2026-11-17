## Description:

Heath Ledger helps agents pull Mercury and optional Stripe financial data, categorize transactions, and generate Excel workbooks for P&L, balance sheet, cash flow, and transaction detail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrannaman](https://clawhub.ai/user/wrannaman)

### License/Terms of Use:


## Use Case:

Developers, finance operators, and external users use this skill to collect Mercury transactions, optionally enrich Stripe revenue and fee data, review categorizations, and produce bookkeeping workbooks for monthly, quarterly, or annual close.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores bank and Stripe credentials plus detailed financial data locally in plaintext.

Mitigation: Use restricted or read-only Mercury and Stripe credentials, install only in a secured local workspace, protect or delete the data directory after use, and rotate credentials used with this version.

Risk: Transaction details and financial records may be exposed through command output, AI categorization workflows, generated data files, and Excel workbooks.

Mitigation: Treat console output, data/heath.db, and generated workbooks as sensitive financial records and avoid sharing them outside approved accounting workflows.

Risk: Financial statements can be inaccurate when Stripe data is unavailable because Mercury shows net payouts and posted transaction dates.

Mitigation: Connect Stripe for exact gross revenue and fees where possible, review ambiguous categorizations, and validate generated books against authoritative accounting records before relying on them.

## Reference(s):

- [Chart of Accounts](references/chart-of-accounts.md)
- [Bookkeeper Comparison](references/bookkeeper-comparison.md)
- [ClawHub Skill Page](https://clawhub.ai/wrannaman/skills/heath-ledger)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands plus generated SQLite data and Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated local data and Excel files may contain sensitive financial records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
