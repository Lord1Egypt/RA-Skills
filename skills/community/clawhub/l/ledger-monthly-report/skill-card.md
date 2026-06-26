## Description: <br>
Generate monthly ledger statistics in CNY with amount and ratio by tag/category, top expense breakdown, and labeled charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and analysts use this skill to generate monthly CNY ledger summaries with income, expense, net amount, ratios, top expense heads, and charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill expects a specific local ledger workspace, virtual environment, data directory, and monthly report script. <br>
Mitigation: Confirm projects/scripts/monthly_report_cny.py, projects/.venv-chart, and projects/data exist before running the report command. <br>
Risk: The default report month is derived from Asia/Taipei time and may not match the user's intended accounting period. <br>
Mitigation: Ask for or specify the month explicitly when the reporting period could be ambiguous. <br>
Risk: Amounts are aggregated using amount_cny, so missing or incorrect CNY-normalized values can affect report accuracy. <br>
Mitigation: Review ledger data for complete amount_cny values before relying on generated totals and ratios. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shing19/ledger-monthly-report) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summary with shell commands, JSON summary output, and PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses amount_cny as the CNY baseline and creates monthly report artifacts under projects/reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
