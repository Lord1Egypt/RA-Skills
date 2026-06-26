## Description: <br>
Monitor system health on the gateway host, including CPU, RAM, disk, temperature, uptime, load, top processes, and alert thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lookupmark](https://clawhub.ai/user/lookupmark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local gateway host health on Raspberry Pi, ARM, or Linux systems and receive threshold-based status alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local system status and process summaries may reveal operational details in the conversation channel. <br>
Mitigation: Use the skill only in channels where local host health summaries and critical alerts are acceptable to share. <br>
Risk: Follow-up repair actions proposed after an alert could affect services, plugins, or logs. <br>
Mitigation: Review and approve any proposed fix command before execution. <br>


## Reference(s): <br>
- [System Monitor on ClawHub](https://clawhub.ai/lookupmark/lookupmark-system-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text status summaries or JSON system health reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CPU, memory, disk, temperature, uptime, load, top process, and alert-threshold details from the local host.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
