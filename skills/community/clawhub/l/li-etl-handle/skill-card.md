## Description: <br>
Li ETL Handle helps agents automate Excel and CSV ETL tasks, including reading, writing, cleaning, transforming, merging, joining, and analyzing spreadsheet data with Node.js. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and operations teams use this skill to automate spreadsheet ETL workflows for trusted Excel and CSV files. It is suited for agent-assisted generation of JavaScript examples, shell commands, configuration guidance, and transformation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unrestricted JavaScript transformation functions. <br>
Mitigation: Use only trusted transformation functions and review generated or supplied scripts before execution. <br>
Risk: Spreadsheet contents may be exposed through logs when sensitive data is processed. <br>
Mitigation: Avoid sensitive data unless logging is disabled, minimized, or controlled in the execution environment. <br>
Risk: The bundled xlsx dependency is reported as a known vulnerable Excel parser. <br>
Mitigation: Process only trusted spreadsheet files and do not treat bundled security reports as proof that dependency risk has been fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-etl-handle) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL documentation](artifact/SKILL.md) <br>
- [Server-resolved publisher profile](https://clawhub.ai/user/43622283) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, package dependencies, and spreadsheet transformation examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
