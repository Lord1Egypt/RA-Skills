## Description: <br>
Monitors local PC resource status, including CPU, memory, disk, network, and available CPU temperature readings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1173910773](https://clawhub.ai/user/1173910773) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check local machine resource usage and produce a quick system status report during troubleshooting or routine monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell wrapper may install psutil into the active Python environment if the dependency is missing. <br>
Mitigation: Install psutil from a trusted package source before use, or run the Python script only after dependencies are already installed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text report or JSON object from local monitoring scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON mode is available with --json; otherwise the script prints a human-readable system report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
