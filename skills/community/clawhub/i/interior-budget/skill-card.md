## Description: <br>
Automatically generates interior design budget spreadsheets by project type, space, and client/project details using standardized templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[137984917-cyber](https://clawhub.ai/user/137984917-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Design studio staff, project managers, and developers use this skill to create editable Excel budget workbooks for home, office, and restaurant interior projects from project name, client, address, area, and type inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workbooks may contain project, client, address, and studio contact details. <br>
Mitigation: Use an explicit output path, review the workbook before sharing, and remove or update contact details when they are not appropriate for the recipient. <br>
Risk: The tool depends on openpyxl to create Excel files. <br>
Mitigation: Install openpyxl from a trusted package source before running the generator. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/137984917-cyber/interior-budget) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Excel workbook plus command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workbooks contain project, client, address, area, budget-line, tax, total, and studio contact fields; openpyxl is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
