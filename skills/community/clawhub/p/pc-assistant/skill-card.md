## Description: <br>
PC Assistant runs cross-platform PC health checks, captures detailed local system diagnostics, and provides actionable recommendations with optional cron scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningtoba](https://clawhub.ai/user/ningtoba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use PC Assistant to run local Windows, macOS, Linux, or WSL diagnostics for storage, CPU, memory, network, services, software, hardware, and security-log checks, then review generated recommendations and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Healthcheck reports may contain sensitive computer, account, network, package, SSH, and security-log details. <br>
Mitigation: Store reports in a private directory with restrictive permissions and redact them before sharing. <br>
Risk: Scheduled healthchecks can create historical records of sensitive local system state. <br>
Mitigation: Enable scheduled runs only when historical tracking is needed and configure cleanup or retention limits. <br>
Risk: The scheduler loads its configuration as shell code. <br>
Mitigation: Keep the scheduler config file private, review it before use, and run the skill as a regular user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ningtoba/pc-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/ningtoba) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; healthcheck runs produce text and JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include sensitive system, account, network, package, SSH, and security-log details.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata and install.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
