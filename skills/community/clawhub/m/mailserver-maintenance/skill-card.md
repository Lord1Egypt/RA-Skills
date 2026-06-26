## Description: <br>
Provides operational runbooks for starting, stopping, checking, and troubleshooting a docker-mailserver deployment, its SMTP relay path, and mail queue issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
System administrators and mailserver operators use this skill to guide an agent through docker-mailserver health checks, relay control, queue inspection, and incident troubleshooting. It is intended for environments where the operator owns the mailserver and remote relay being administered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live mailserver, remote relay, shutdown, restart, and queue-flush operations. <br>
Mitigation: Install only for mail infrastructure you own or administer, and require explicit operator confirmation before disruptive actions. <br>
Risk: The runbook includes a hardcoded external email health-check target. <br>
Mitigation: Replace it with a controlled test mailbox or require confirmation before sending any test message. <br>
Risk: The SSH configuration disables strict host key checking. <br>
Mitigation: Configure host key verification before use and document the expected Docker and SSH prerequisites. <br>


## Reference(s): <br>
- [Mailserver architecture reference](references/architecture.md) <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/mailserver-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operational guidance should be reviewed before execution on live mail infrastructure.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
