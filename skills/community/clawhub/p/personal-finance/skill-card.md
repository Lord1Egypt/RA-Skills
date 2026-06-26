## Description: <br>
Manage personal finances, track spending by category, set budgets, and receive reminders for EMIs and one-time annual expenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aka-anoop](https://clawhub.ai/user/aka-anoop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and agents use this skill to log expenses, organize spending by preset or custom categories, set budgets, and manage EMI or annual payment reminders in a local SQLite database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal finance amounts, categories, budgets, and reminders in a local SQLite file. <br>
Mitigation: Use the skill only when local storage is acceptable, confirm write actions before records are added, and delete or back up finance.db according to privacy needs. <br>


## Reference(s): <br>
- [Personal Finance Data](references/finance_data.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aka-anoop/personal-finance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local SQLite record updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores expense amounts, categories, budgets, and payment reminders locally in finance.db] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
