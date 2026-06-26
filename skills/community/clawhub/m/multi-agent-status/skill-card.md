## Description: <br>
Cross-agent health monitoring for multi-host OpenClaw deployments. Each agent pushes structured status reports (JSON) to a central location. A PM/monitoring agent reads them and alerts on failures. Works across Windows, Linux, and mixed environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenthyjack](https://clawhub.ai/user/agenthyjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up shared status reporting across multiple OpenClaw agents, then monitor gateway health, cron errors, stale reports, and missing reports from a central dashboard or monitoring agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Overly permissive shared-directory permissions could allow unauthorized status report writes or tampering. <br>
Mitigation: Replace chmod 777 with a dedicated user or group and restrictive permissions such as 750 or 770 before installation. <br>
Risk: Remote status uploads rely on SSH and could broaden access if reused with an unrestricted key or unverified destination. <br>
Mitigation: Use a limited SSH key for uploads and validate the destination host. <br>
Risk: Status reports may expose operational details beyond what the monitor needs. <br>
Mitigation: Keep reported status fields to the minimum needed for health monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agenthyjack/multi-agent-status) <br>
- [Collective Skills references](https://github.com/Bobalouie44/collective-skills/tree/main/references) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and PowerShell code blocks plus JSON status report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions for scheduled status reports and a monitoring-agent dashboard workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
