## Description: <br>
Convert 电力交易/电网边界条件 96点数据 into 24点小时数据 by averaging each consecutive 4 quarter-hour rows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mecyalika](https://clawhub.ai/user/mecyalika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to convert electricity-trading Excel workbooks from 96 quarter-hour rows into 24 hourly averages, and to repair templates whose 24-point formulas reference the wrong source columns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overwrite or alter an existing business-critical workbook if used carelessly. <br>
Mitigation: Work on a copy, keep backups of important templates, and avoid overwriting the only version of a spreadsheet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mecyalika/power-trading-96-to-24) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated Excel workbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create source96, result24, and formula24 sheets or minimally update an existing xlsx template.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
