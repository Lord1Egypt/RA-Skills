## Description: <br>
从DXF提取户型信息，并结合历史报价库生成匹配模板的家装或工装预算Excel。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[137984917-cyber](https://clawhub.ai/user/137984917-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Interior designers and renovation estimators use this skill to turn exported DXF floor-plan files and a local historical pricing library into editable Excel budget drafts for residential or commercial projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated spreadsheets can expose internal pricing assumptions from the local budget library. <br>
Mitigation: Review the budget library and generated workbook before sharing the output with clients or external parties. <br>
Risk: The default budget-library path is machine-specific and may not match the user's environment. <br>
Mitigation: Confirm or update the local budget-library path before running the script. <br>
Risk: Writing to an existing output path can replace a prior spreadsheet. <br>
Mitigation: Choose an output path where overwriting an existing file would be acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/137984917-cyber/interior-auto-budget) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Excel workbook (.xlsx) with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python dependencies, a local JSON budget library, and a user-supplied DXF input file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
