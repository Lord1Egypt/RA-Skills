## Description: <br>
Standard operating procedures for agent maintenance, security hygiene, and system health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staybased](https://clawhub.ai/user/staybased) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run recurring maintenance, security hygiene, memory upkeep, secret scans, dependency checks, health checks, and incident-response routines for an agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The heartbeat dispatcher can use a stored mail API key to check a fixed AgentMail inbox that the user did not configure. <br>
Mitigation: Review or edit the heartbeat script before installation, remove or parameterize the hard-coded inbox, and require explicit opt-in before reading .secrets or checking mail. <br>
Risk: Recurring maintenance scripts can preserve sensitive information in memory logs, git reminders, or secret-scan output if run without supervision. <br>
Mitigation: Supervise recurring runs and review generated logs and alerts so operational details and scan findings are not retained unintentionally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/staybased/ops-hygiene) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON status output from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes maintenance cadences, checklist state guidance, and shell scripts for health checks, secret scanning, security audits, and heartbeat alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
