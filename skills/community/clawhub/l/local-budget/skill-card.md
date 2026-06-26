## Description: <br>
Analyze exported bank and credit card CSV files locally to normalize transactions, suggest spending categories, compare actual spending against budgets, and generate markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze personal finance CSV exports, review suggested transaction categories, compare spending against a local budget file, and produce an Obsidian-compatible spending report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank and credit-card exports can contain sensitive financial data. <br>
Mitigation: Keep input CSVs, generated JSON files, and markdown reports in a private local folder, and avoid synced or shared vaults unless intentional. <br>
Risk: Suggested categories may be wrong for ambiguous or low-confidence transactions. <br>
Mitigation: Review low- and medium-confidence categorizations before relying on budget totals or reports. <br>


## Reference(s): <br>
- [Spending Categories Reference](references/categories.md) <br>
- [CSV Format Reference](references/csv-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON transaction files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written locally; categorization includes confidence values and requires review for low- or medium-confidence transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
