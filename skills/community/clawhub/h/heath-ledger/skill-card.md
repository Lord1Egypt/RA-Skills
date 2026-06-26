## Description: <br>
AI bookkeeping agent for Mercury bank accounts that pulls transactions, categorizes them with rules and optional AI, and generates Excel workbooks with P&L, Balance Sheet, Cash Flow, and transaction detail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrannaman](https://clawhub.ai/user/wrannaman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, finance operators, and developers use this skill to connect Mercury and optionally Stripe, categorize bank transactions, reconcile bookkeeping data, and produce monthly, quarterly, or annual financial workbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank and Stripe API credentials are stored in plaintext local state. <br>
Mitigation: Run the skill only in a protected local environment, use limited-scope or read-only keys where available, and rotate or revoke credentials after use. <br>
Risk: Transaction counterparties, descriptions, amounts, and other financial details may appear in terminal output or AI categorization prompts. <br>
Mitigation: Protect terminal logs and avoid AI categorization unless sharing transaction details with the host model workflow is acceptable. <br>
Risk: Generated bookkeeping outputs can be inaccurate when Mercury data lacks exact Stripe gross revenue, fees, transaction counts, timing adjustments, or journal entries. <br>
Mitigation: Review generated workbooks before relying on them, connect Stripe for exact revenue and fee data when available, and have a qualified reviewer validate accounting treatment. <br>


## Reference(s): <br>
- [Heath Ledger ClawHub Page](https://clawhub.ai/wrannaman/heath-ledger) <br>
- [Publisher Profile](https://clawhub.ai/user/wrannaman) <br>
- [Chart of Accounts](references/chart-of-accounts.md) <br>
- [Bookkeeper Comparison](references/bookkeeper-comparison.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON categorization prompts, local SQLite state, and generated Excel workbook files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bookkeeping reports and transaction categorizations; generated outputs may include sensitive financial data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
