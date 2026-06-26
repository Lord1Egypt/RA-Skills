## Description: <br>
AI project management assistant for planning, tracking, and managing projects using predictive, adaptive, and hybrid methodologies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CyberneticsPlus](https://clawhub.ai/user/CyberneticsPlus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers use this skill to structure project charters, work breakdown structures, schedules, risk registers, RACI matrices, earned value calculations, sprint forecasts, health checks, and status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health checks may inspect filenames and modification times in project folders selected by the user. <br>
Mitigation: Run health checks only against project directories that are appropriate for the assistant to inspect. <br>
Risk: Risk scoring can read a JSON file explicitly provided by the user. <br>
Mitigation: Provide only risk files intended for project-management analysis and review outputs before using them for decisions. <br>
Risk: Project-management recommendations and generated plans may be incomplete or based on uncertain estimates. <br>
Mitigation: Have accountable project stakeholders review charters, schedules, budgets, risks, and change decisions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CyberneticsPlus/pmp-agentclaw) <br>
- [README](artifact/README.md) <br>
- [Simple Guide](artifact/SIMPLE_GUIDE.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Copyright and Trademark Disclaimer](artifact/DISCLAIMER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, TypeScript API results, and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read explicitly provided project directories for health checks and explicitly provided JSON risk files for scoring.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
