## Description: <br>
Generates Morgan Stanley-style DCF/SOTP financial model Excel workbooks with scenario valuation, WACC, sensitivity, PE band, comps, KPI, and chart sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjkj999999](https://clawhub.ai/user/yjkj999999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External analysts, finance professionals, and agents supporting financial modeling use this skill to create Excel workbooks for DCF/SOTP valuation, scenario analysis, comparable companies, PE band analysis, and operational KPI dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local Excel files and could overwrite an existing workbook if the same output path is reused. <br>
Mitigation: Choose a deliberate output path and check for existing files before running the generator. <br>
Risk: Generated valuation workbooks may contain assumptions or financial outputs that are inappropriate for a real investment decision. <br>
Mitigation: Independently review company data, forecast assumptions, formulas, and valuation conclusions before relying on the workbook. <br>
Risk: The workbook defaults to Chinese labels unless English output is requested. <br>
Mitigation: Use the English language option when the reviewer or recipient needs English workbook output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yjkj999999/ms-financial-model) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; when executed, creates .xlsx workbook files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python >= 3.9 and openpyxl >= 3.1; default workbook language is zh with an en option.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
