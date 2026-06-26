## Description: <br>
Analyzes monthly financial reports for Hainan Shouqianba Technology and Suzhou Wosai Technology by extracting ledger or account-balance data, preparing the three financial statements, updating Feishu templates, and producing an analysis summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operators and reporting agents use this skill to prepare monthly report analysis for two named company entities, validate ledger or balance-sheet inputs, update Feishu reporting templates, and produce concise management commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update persistent Feishu financial templates under broad monthly-report triggers without explicit confirmation or rollback safeguards. <br>
Mitigation: Before any write or cleanup operation, confirm the company, reporting month, source spreadsheet, target Feishu document, sheet, and exact cell ranges, then require a preview or manual approval. <br>
Risk: Incorrect source spreadsheets, sheet selection, or cell ranges could produce misleading financial statements or overwrite formula columns. <br>
Mitigation: Read the template layout before writing, preserve formula columns, and use the skill's trial-balance and cross-check steps to verify figures before final updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/monthly-report-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Spreadsheet updates, Guidance] <br>
**Output Format:** [Markdown analysis summary with structured Feishu spreadsheet updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial figures are expected to be rounded to ten-thousand yuan units with one decimal place where the skill requests narrative analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
