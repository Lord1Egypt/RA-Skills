## Description: <br>
Personal expense tracker - record expenses, auto-categorize, monthly statistics with total and category breakdown <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to record personal expenses, auto-categorize entries, list recent spending, and view monthly category statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal financial records and monthly spending summaries are stored locally, including a summary written by the stats command. <br>
Mitigation: Install only when local storage of personal expense data is acceptable, protect the local data files, and remove or change the stats-command summary write if that extra copy is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/personal-expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Command-line text output and JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores expense records in ~/.expense-tracker/expenses.json and writes monthly summary data from the stats command.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
