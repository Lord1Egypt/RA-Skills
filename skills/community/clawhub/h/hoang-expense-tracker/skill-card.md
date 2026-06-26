## Description: <br>
AI Expense Tracker helps users log personal spending, generate spending reports with charts, set category budgets, and receive lighthearted spending feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoanghust2003](https://clawhub.ai/user/hoanghust2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using an agent use this skill to record expense amounts, categories, and descriptions, review spending summaries and charts, and get budget or spending feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal spending records and chart images locally outside its own skill folder. <br>
Mitigation: Before using real personal finance details, confirm the storage paths for expenses.csv and expense_chart.png and periodically review or delete those files. <br>
Risk: Expense logging changes local records and the skill does not provide strong scoping or deletion controls. <br>
Mitigation: Confirm the amount, category, description, and date before logging an expense, and avoid sensitive descriptions. <br>
Risk: Spending feedback may include playful roast-style language based on local expense data. <br>
Mitigation: Keep generated feedback light, non-abusive, and focused on budget guidance rather than personal judgment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hoanghust2003/hoang-expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Agent-facing instructions with command outputs as JSON and user-facing text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local expenses.csv spending records and expense_chart.png report images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
