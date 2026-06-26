## Description: <br>
Administer IT by monitoring security and configuring Google Workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT administrators use this persona to monitor Google Workspace security signals, review pending IT requests, and prepare Workspace policy or configuration changes with dry-run checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace administration actions can affect users, groups, organizational units, or sharing policies when run with broad service-account permissions. <br>
Mitigation: Use a dedicated least-privilege service account, verify gws auth status, scope changes to named targets, and require dry-runs plus explicit approval before bulk or policy-changing actions. <br>
Risk: Security and administration guidance may be incomplete if the agent lacks the required Google Workspace utility skills or current admin context. <br>
Mitigation: Load gws-gmail, gws-drive, and gws-calendar before use, then review proposed actions against current Workspace policy before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/persona-it-admin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-gmail, gws-drive, and gws-calendar utility skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence; artifact metadata version: 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
