## Description: <br>
Expense Tracker helps an agent log natural-language spending, categorize expenses, track budgets, and generate weekly or monthly reports using local JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicholasrae](https://clawhub.ai/user/nicholasrae) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to maintain a local personal expense ledger, check category spending against monthly budgets, and request spending summaries or reports through conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal spending history is stored as plain local JSON in the skill folder. <br>
Mitigation: Keep the skill folder private, restrict filesystem access, and back up expenses/ledger.json if the records matter. <br>
Risk: The skill can change or delete ledger entries and budget settings during normal use. <br>
Mitigation: Ask the agent to confirm before deleting, recategorizing, or changing budgets, and review proposed changes before execution. <br>


## Reference(s): <br>
- [Expense Tracker ClawHub release page](https://clawhub.ai/nicholasrae/nicholasrae-expense-tracker) <br>
- [categories.json](references/categories.json) <br>
- [budgets.json](references/budgets.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration] <br>
**Output Format:** [Conversational text, Markdown reports, shell command invocations, and local JSON ledger or budget updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, jq, and bc on macOS or Linux; stores expense records locally in expenses/ledger.json.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
