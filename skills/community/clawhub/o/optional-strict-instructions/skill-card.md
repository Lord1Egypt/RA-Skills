## Description: <br>
Handle operations requiring user confirmation, permission verification, and strict adherence to explicit instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhangWud1](https://clawhub.ai/user/ZhangWud1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through sensitive system tasks such as sudo operations, file deletion or modification, package installation, service management, and system configuration changes. It emphasizes checking resources, presenting clear choices, waiting for explicit confirmation, and reporting failures without bypassing permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled shell helper can execute arbitrary commands with sudo and may handle sudo passwords unsafely. <br>
Mitigation: Manually inspect any sudo, delete, package-install, service-management, account, database, or system-configuration command before approval, and do not provide sudo passwords through agent prompts or script arguments. <br>
Risk: Sensitive operations can permanently modify files, services, accounts, packages, databases, or system configuration. <br>
Mitigation: Use the skill's confirmation checklist as guidance only, prefer dry runs or backups where available, and require explicit user approval before execution. <br>


## Reference(s): <br>
- [Detailed Scenarios for Optional Strict Instructions](references/scenarios.md) <br>
- [ClawHub skill page](https://clawhub.ai/ZhangWud1/optional-strict-instructions) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and option lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confirmation prompts, verification checklists, and execution-result reporting patterns.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
