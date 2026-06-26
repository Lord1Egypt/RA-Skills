## Description: <br>
Return system metrics (CPU, RAM, disk, processes) using psutil. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyeque](https://clawhub.ai/user/iyeque) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect local CPU, memory, disk, and process metrics from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The processes action can reveal local usernames and running program names in the agent session. <br>
Mitigation: Avoid using the processes action on shared or sensitive machines unless that information can be exposed to the session. <br>
Risk: The skill depends on the psutil Python package. <br>
Mitigation: In controlled environments, install psutil from an approved package source or pin an approved version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iyeque/iyeque-local-system-info) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON printed to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions include summary, cpu, memory, disk, and processes; process output can include PID, process name, username, CPU percent, and memory percent.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence.release.version, metadata.openclaw.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
