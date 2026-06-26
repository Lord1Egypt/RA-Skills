## Description: <br>
Host security hardening and risk-tolerance configuration for OpenClaw deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to assess host security posture, review firewall, SSH, update, backup, exposure, and OpenClaw audit status, and plan staged remediation without disrupting access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Host hardening guidance may include commands that change firewall, SSH, update, service, cron, or memory-writing behavior. <br>
Mitigation: Review each proposed command and approve only after confirming access preservation, impact, and rollback steps. <br>
Risk: Remote access changes can lock a user out of a machine if applied without confirming the connection path. <br>
Mitigation: Confirm how the user connects before changing remote access settings, and prefer staged, reversible changes with a rollback plan. <br>
Risk: Security checks may expose sensitive host details in command output or logs. <br>
Mitigation: Redact secrets and sensitive host details, avoid logging credentials, and store audit outputs only in a user-approved location. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and numbered user choices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before state-changing host security actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
