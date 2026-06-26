## Description: <br>
Provides system monitoring, performance analysis, and status information for NVIDIA Jetson devices, including GPU, CPU, memory, temperature, and JetPack version checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxd9199](https://clawhub.ai/user/wxd9199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect NVIDIA Jetson device status, monitor system performance, and gather GPU, CPU, memory, disk, temperature, and JetPack-related information during development or operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command output can expose hardware, system, and environment details that may be sensitive. <br>
Mitigation: Avoid sharing Jetson status output publicly unless hardware and system details have been reviewed for sensitivity. <br>
Risk: The skill depends on local Jetson utilities such as tegrastats and jetson_release. <br>
Mitigation: Use Jetson and OS package sources you trust when installing or invoking these dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxd9199/jetson-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command-output-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local hardware and system status details from Jetson monitoring tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
