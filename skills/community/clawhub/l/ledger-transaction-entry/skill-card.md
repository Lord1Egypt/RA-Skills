## Description: <br>
Convert natural-language spending/income statements into ledger JSONL records and append them into projects/data/YYYY/YYYY-MM.jsonl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal finance users use this skill to turn natural-language transaction notes into structured ledger entries, append them to monthly JSONL files, and generate monthly summary charts from local ledger data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local ledger entries and can generate local reports, so an incorrect parse or target path could create unwanted bookkeeping changes. <br>
Mitigation: Use it only in projects where projects/data and projects/reports are intended locations, and preview parsed fields or target files before writing when mistakes would be costly. <br>
Risk: Monthly summaries may combine amounts across currencies when source data contains multiple currencies. <br>
Mitigation: Review the skill's mixed-currency note and convert entries to a single base currency before relying on totals for financial decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [JSONL ledger records, PNG charts, and text confirmations with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends records under projects/data/YYYY/YYYY-MM.jsonl and may generate local reports under projects/reports/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
