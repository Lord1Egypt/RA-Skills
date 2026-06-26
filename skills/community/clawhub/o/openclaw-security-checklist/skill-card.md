## Description: <br>
OpenClaw Security Checklist helps developers and operators run pre-deployment security and compliance checks for OpenClaw deployments, covering firewall, SSH, API key handling, data-border considerations, and Mac, VPS, Docker, and enterprise scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiyuanlu](https://clawhub.ai/user/yiyuanlu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill before deploying OpenClaw to check baseline security controls, review compliance-sensitive configuration, and produce shareable Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can include raw lines that match secret-like patterns from local OpenClaw workspace files. <br>
Mitigation: Review and redact generated reports before sharing, run checks in a controlled workspace, and rotate any credential that appears in report output. <br>
Risk: The security check can read local OpenClaw configuration and workspace files while evaluating API key and deployment settings. <br>
Mitigation: Review the script before running it on sensitive systems and limit execution to environments where local configuration inspection is acceptable. <br>
Risk: The data-border check can make an outbound request to ipinfo.io when curl is available. <br>
Mitigation: Run the check only where that network lookup is acceptable, or review and disable the location check before execution. <br>


## Reference(s): <br>
- [Openclaw Security Checklist on ClawHub](https://clawhub.ai/yiyuanlu/openclaw-security-checklist) <br>
- [API Key Management](references/api-key-management.md) <br>
- [China Compliance Checklist](references/compliance-cn.md) <br>
- [Data Border Checklist](references/data-border.md) <br>
- [Personal Mac Deployment Checklist](references/deployment-scenarios/personal-mac.md) <br>
- [VPS Deployment Checklist](references/deployment-scenarios/vps.md) <br>
- [Docker Deployment Checklist](references/deployment-scenarios/docker.md) <br>
- [Enterprise Deployment Checklist](references/deployment-scenarios/enterprise.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and checklist guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local Markdown or text reports from host and OpenClaw workspace checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
