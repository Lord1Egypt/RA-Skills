## Description: <br>
Stream recent logs from the systemd journal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for recent systemd journal logs by service unit, line count, and follow mode when troubleshooting local Linux systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Journal logs can expose system paths, usernames, application data, or secrets. <br>
Mitigation: Keep requests scoped to the needed service and line count, and review log output before sharing it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires journalctl on a systemd-based Linux system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
