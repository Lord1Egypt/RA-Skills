## Description: <br>
Passive financial tracking plugin for PhoenixClaw that detects expenses and income from conversations and payment screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goforu](https://clawhub.ai/user/goforu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External PhoenixClaw users use this skill to add passive personal finance tracking, including transaction extraction, categorization, budgets, reports, goals, trends, and natural-language finance queries. It is intended for users who explicitly want conversations, memory, and payment screenshots converted into local financial records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill passively turns conversations, memory, and payment screenshots into a persistent local financial history. <br>
Mitigation: Enable it only when the user intentionally wants passive financial tracking, and confirm how to disable auto-recording, review or undo entries, and delete stored receipts and reports. <br>
Risk: Stored receipts, reports, and ledger files may expose sensitive transaction data if kept in cloud-synced or shared folders. <br>
Mitigation: Keep the finance directory out of cloud-synced or shared locations and restrict access to local files containing financial records. <br>
Risk: Cross-plugin insight sharing may correlate spending with mood, social, or other personal data. <br>
Mitigation: Turn off cross-plugin insight sharing unless the user explicitly wants those correlations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/goforu/phoenixclaw-ledger) <br>
- [Expense Detection from Conversations](artifact/references/expense-detection.md) <br>
- [Payment Screenshot Recognition](artifact/references/payment-screenshot.md) <br>
- [Merchant to Category Mapping](artifact/references/merchant-category-map.md) <br>
- [Category Rules and Definitions](artifact/references/category-rules.md) <br>
- [Budget Tracking](artifact/references/budget-tracking.md) <br>
- [Financial Insights Generation](artifact/references/financial-insights.md) <br>
- [Cron Setup for PhoenixClaw Ledger](artifact/references/cron-setup.md) <br>
- [Financial Goal Management](artifact/references/goal-management.md) <br>
- [Real-time Financial Query Patterns](artifact/references/query-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown reports and journal sections with YAML ledger, budget, goal, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local financial history, receipt references, scheduled report guidance, and budget or goal status summaries.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
