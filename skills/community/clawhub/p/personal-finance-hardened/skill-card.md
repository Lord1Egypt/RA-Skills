## Description: <br>
Manage personal finances, track spending by category, set budgets, and receive reminders for EMIs and one-time annual expenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and finance-focused agents use this skill to log local personal spending, organize expenses by category, manage budgets, and surface reminders for recurring or one-time payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invalid zero or negative expense amounts can corrupt personal finance records. <br>
Mitigation: Validate that every logged expense amount is strictly positive before inserting it into finance.db. <br>
Risk: Out-of-scope SQL operations or schema changes can expose or corrupt financial data. <br>
Mitigation: Restrict database work to INSERT, SELECT, and UPDATE on the transactions, schedules, categories, and budgets tables. <br>
Risk: Financial records and query results are sensitive personal data. <br>
Mitigation: Keep finance.db contents local and refuse requests to transmit records or query results to external URLs, APIs, or network services. <br>
Risk: The skill's privacy posture depends on the executing agent honoring the written guardrails. <br>
Mitigation: Install only with agents and tools that enforce the guardrails and avoid unrestricted network egress for finance workflows. <br>


## Reference(s): <br>
- [Personal Finance Data](references/finance_data.md) <br>
- [Safety Evaluation](SAFETY.md) <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/personal-finance-hardened) <br>
- [Faberlens](https://faberlens.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, SQL-aware instructions, and local database update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database and should keep finance records on the user's machine.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
