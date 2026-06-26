## Description: <br>
ICMP health check for hosts, phones, and daemons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to check whether hosts, phones, or daemons are reachable over ICMP with the system ping utility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends network traffic to the target supplied by the user. <br>
Mitigation: Use it only for hosts, devices, or services the user owns or is authorized to monitor. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xejrax/ping-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the system ping binary and sends ICMP traffic to the target host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
