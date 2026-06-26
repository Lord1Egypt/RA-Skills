## Description: <br>
Local SQLite bookkeeping skill for Chinese natural-language requests to record, query, categorize, update, and delete financial transactions, wallet accounts, balances, recurring transactions, and period reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanmwx](https://clawhub.ai/user/seanmwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal finance agents use this skill to manage local bookkeeping in Chinese, including transaction entry, wallet and category maintenance, balance checks, recurring schedules, and day/week/month/year analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately modify or delete local financial records, including deleting the latest entry. <br>
Mitigation: Keep backups of the SQLite database and review destructive commands before execution, especially vague deletion requests. <br>
Risk: Command outputs may contain sensitive transaction details. <br>
Mitigation: Treat outputs as private financial data and avoid sharing logs or summaries outside the intended user context. <br>
Risk: Period reports with multiple currencies use raw stored amounts without foreign-exchange conversion. <br>
Mitigation: State when mixed-currency totals are raw amounts and avoid presenting them as converted portfolio totals. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seanmwx/money-tracker) <br>
- [Command reference](references/commands.md) <br>
- [Intent mapping](references/intent_mapping.md) <br>
- [Chat reference](references/chat_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise natural-language responses with JSON-producing shell command calls and summarized bookkeeping results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database and Python standard library; day/week/month/year reports preserve raw stored amounts without FX conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
