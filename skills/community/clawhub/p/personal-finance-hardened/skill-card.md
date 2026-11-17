## Description:

Manage personal finances, track spending by category, set budgets, and receive reminders for EMIs and one-time annual expenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to log personal expenses, review budget status, and manage reminders for recurring EMIs and annual expenses while keeping records local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and maintains a local finance.db file containing personal financial records.

Mitigation: Install only when local storage of financial records is acceptable, and keep the database under the user's control.

Risk: Financial records or query results could expose sensitive personal information if sent to external services.

Mitigation: Keep the no-network guardrail in place and do not export, sync, or POST finance.db contents or query results to external URLs, APIs, or network services.

Risk: Invalid expense amounts or out-of-scope SQL operations could corrupt financial records or expand database access beyond the intended tables.

Mitigation: Reject zero or negative expense amounts and limit database operations to INSERT, SELECT, and UPDATE on the intended finance tables.

## Reference(s):

- [Personal Finance Data](references/finance_data.md)
- [Safety Evaluation](SAFETY.md)
- [Faberlens Personal Finance Safety Evaluation](https://faberlens.ai/explore/personal-finance)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/personal-finance-hardened)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured finance summaries and inline shell commands when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and maintain a local SQLite finance.db file through permitted local operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
