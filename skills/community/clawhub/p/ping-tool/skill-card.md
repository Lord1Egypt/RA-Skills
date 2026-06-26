## Description: <br>
Test network connectivity to remote hosts by sending ICMP echo requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network operators use this skill to check basic reachability and latency for hosts they own, manage, or have permission to test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ping requests can be inappropriate or disruptive when directed at systems the user does not own or have permission to test. <br>
Mitigation: Use the skill only for hosts the user owns, manages, or is authorized to test. <br>
Risk: The documented command options are broader than the bundled script behavior, which always sends four pings and only accepts a host argument. <br>
Mitigation: Treat option examples as usage guidance for a ping tool, and verify actual script behavior before relying on custom packet count, interval, size, or timeout settings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script runs four ping requests against a provided host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
