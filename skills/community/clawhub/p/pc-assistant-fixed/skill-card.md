## Description: <br>
PC healthcheck and diagnostics with detailed system information and actionable recommendations. Works on Windows, macOS, and Linux. Read-only system diagnostics. Supports scheduling via cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningtoba](https://clawhub.ai/user/ningtoba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support staff, and power users use this skill to run local PC diagnostics, collect system health reports, and receive maintenance recommendations for Windows, macOS, Linux, or WSL systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can contain sensitive system, user, package, network, SSH, and security-log information. <br>
Mitigation: Store reports in a private local directory, avoid sharing them publicly, and redact sensitive values before sending them to another person or service. <br>
Risk: Scheduled healthchecks can repeatedly collect sensitive local diagnostics and retain them on disk. <br>
Mitigation: Use scheduled runs only with a controlled config file and cron entry, choose a private output directory, and enable cleanup for old reports when appropriate. <br>
Risk: Running broad diagnostics with elevated privileges can expose more local security data than needed. <br>
Mitigation: Run the skill as a normal user unless a specific check requires otherwise, and review the script behavior before installation or automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ningtoba/pc-assistant-fixed) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Timestamped plain-text healthcheck reports, JSON summaries, shell command invocations, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written to local output directories and may contain sensitive system, user, package, network, SSH, and security-log information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
