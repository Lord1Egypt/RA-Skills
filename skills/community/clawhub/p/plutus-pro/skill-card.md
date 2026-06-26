## Description: <br>
Plutus Pro analyzes expense CSVs or pasted transaction text to categorize spending, compare budgets, flag tax-deductible categories, forecast spending, calculate savings rate, and export local reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn bank or app transaction exports into monthly expense, budget, tax-category, savings-rate, P&L, and spending-forecast reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes transaction data and saves generated expense reports locally by default. <br>
Mitigation: Run it only in a directory you control, and protect or delete generated plutus_pro_report, plutus_pro_summary, and plutus_pro_data files after use. <br>
Risk: The setup instructions install Python dependencies into the active Python environment. <br>
Mitigation: Prefer a virtual environment for dependency installation instead of modifying the system Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/plutus-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with bash and Python code blocks; generated Markdown, CSV, and JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LICENSE_KEY and optionally reads EXPENSES_FILE, EXPENSES_TEXT, BUDGET_JSON, SAVINGS_GOAL, TAX_CATEGORIES, CURRENCY, REPORT_MONTH, and FORECAST_MONTHS.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
