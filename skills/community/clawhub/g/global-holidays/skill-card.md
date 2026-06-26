## Description: <br>
Global Holidays helps agents check, generate, and work with public holidays for countries, subdivisions, date ranges, business-day workflows, and explicitly provided custom holiday dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yting27](https://clawhub.ai/user/yting27) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users use this skill to answer public holiday questions, list holidays by country or subdivision, find holidays in date ranges, support business-day calculations, and merge official holidays with user-provided custom dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned package installation can change holiday data or behavior over time. <br>
Mitigation: Use a virtual environment and pin the holidays package version when reproducible behavior is required. <br>
Risk: Custom holiday JSON loading can read a local file path supplied during use. <br>
Mitigation: Only load custom holiday files when the user explicitly provides the path, and verify the file exists before reading it. <br>


## Reference(s): <br>
- [Global Holidays on ClawHub](https://clawhub.ai/yting27/global-holidays) <br>
- [holidays Python package](https://pypi.org/project/holidays/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and pip with the holidays package installed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
