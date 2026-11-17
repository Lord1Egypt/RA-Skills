## Description:

PhoenixClaw Ledger passively detects expenses and income from conversations and payment screenshots, then creates local ledger data, journal finance sections, and scheduled reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goforu](https://clawhub.ai/user/goforu)

### License/Terms of Use:


## Use Case:

External PhoenixClaw users use this skill to track personal finances with minimal manual entry, including expense detection, categorization, budgets, goals, and finance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill passively reads money-related conversations and payment screenshots.

Mitigation: Install only when this access is acceptable, and review or disable screenshot auto-recording and passive finance scanning if tighter privacy is needed.

Risk: The skill creates local ledgers, receipt files, journal summaries, and scheduled reports containing financial details.

Mitigation: Review storage locations, journal export behavior, cron jobs, and cross-plugin sharing before deployment.

Risk: Automatically generated financial summaries may expose sensitive transaction history in journals or reports.

Mitigation: Limit who can access PhoenixClaw journal and finance directories, and review generated summaries before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goforu/skills/phoenixclaw-ledger)
- [Budget Tracking](references/budget-tracking.md)
- [Category Rules and Definitions](references/category-rules.md)
- [Cron Setup for PhoenixClaw Ledger](references/cron-setup.md)
- [Expense Detection from Conversations](references/expense-detection.md)
- [Financial Goal Management](references/goal-management.md)
- [Financial Insights Generation](references/financial-insights.md)
- [Merchant to Category Mapping](references/merchant-category-map.md)
- [Payment Screenshot Recognition](references/payment-screenshot.md)
- [Real-time Financial Query Patterns](references/query-patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown reports and journal sections, YAML ledger and configuration data, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduled report guidance and local PhoenixClaw journal or finance file paths.]

## Skill Version(s):

0.0.2 (source: server release metadata; artifact metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
