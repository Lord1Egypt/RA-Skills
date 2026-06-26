## Description: <br>
Analyze exported bank/credit card CSV files locally to track spending, categorize transactions with LLM reasoning, compare against user-defined budgets, and generate markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to analyze local bank or credit card CSV exports, categorize transactions, compare spending against budgets, and generate markdown finance reports. It is suited for privacy-sensitive personal budgeting workflows where raw financial files stay local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive bank CSVs and can write intermediate JSON and markdown reports containing transaction details. <br>
Mitigation: Keep raw CSVs, generated JSON, and reports in private local folders, and avoid shared or synced vaults unless that storage is intended. <br>
Risk: Automated transaction categorization can produce incorrect budget conclusions. <br>
Mitigation: Review suggested categories, especially low-confidence or uncategorized transactions, before relying on the final report. <br>


## Reference(s): <br>
- [Local Budget ClawHub Release](https://clawhub.ai/newageinvestments25-byte/nai-local-budget) <br>
- [Spending Categories Reference](references/categories.md) <br>
- [CSV Format Reference](references/csv-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and generated markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSON intermediates and Obsidian-compatible markdown reports from user-provided transaction CSVs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
