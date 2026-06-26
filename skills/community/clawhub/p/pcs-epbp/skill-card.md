## Description: <br>
从 PCS 页面抓取表格数据，导出 Excel 文件，并上传导入到 EBP 系统。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shandongwill](https://clawhub.ai/user/shandongwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations or platform automation users use this skill to move PCS table data into EBP through a generated Excel file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic upload into EBP can move operational PCS data without built-in review safeguards. <br>
Mitigation: Test with non-production data first, inspect the generated Excel file, and add a human approval step before upload. <br>
Risk: Unattended cron scheduling can repeat imports or hide failures if duplicate prevention and monitoring are absent. <br>
Mitigation: Enable duplicate checks, logging, monitoring, and recovery procedures before scheduled unattended runs. <br>
Risk: Browser automation depends on internal pages and selectors that may change. <br>
Mitigation: Validate selectors after PCS or EBP UI changes and fail closed when expected tables or upload controls are absent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shandongwill/pcs-epbp) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Excel file plus browser automation status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes pcs_data.xlsx and uploads it to EBP when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
