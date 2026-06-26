## Description: <br>
Scans a macOS or Linux host for Docker containers, system services, and listening TCP ports, then generates a human-readable Markdown homelab runbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and homelab administrators use this skill to inventory local services and produce a runbook for maintenance, troubleshooting, or documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated runbooks can expose sensitive local system details, including running services, containers, mounts, open ports, processes, and PIDs. <br>
Mitigation: Treat runbooks as sensitive operational documents, review and redact them before sharing, and store output only in trusted locations. <br>
Risk: Scheduled or repeated runs can accumulate fresh host inventory data in files the user may forget about. <br>
Mitigation: Use scheduled runs only after confirming the output path, retention expectations, and access controls. <br>


## Reference(s): <br>
- [Customization Guide](references/customization.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/homelab-runbook) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown runbook with concise agent summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the runbook to a user-specified file path; scanner JSON is an intermediate input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
