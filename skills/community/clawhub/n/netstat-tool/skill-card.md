## Description: <br>
Display network connections, routing tables, and interface statistics for network diagnostics and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to ask an agent to inspect local listening TCP and UDP sockets during network troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes local listening port and socket information, which may reveal service inventory or network configuration. <br>
Mitigation: Run it only where the agent is authorized to inspect network diagnostics, and avoid sharing output outside the intended troubleshooting context. <br>
Risk: The advertised command options are broader than the current behavior, which runs a fixed netstat -tuln command. <br>
Mitigation: Treat results as listening TCP and UDP socket output, and verify behavior before relying on options such as process, routing, or interface views. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs netstat -tuln; advertised CLI options may not be honored by the current script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
