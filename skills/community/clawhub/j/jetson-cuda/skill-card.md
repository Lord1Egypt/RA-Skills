## Description: <br>
Provides NVIDIA Jetson CUDA tools to query CUDA version, GPU device information, and CUDA library paths on Jetson devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxd9199](https://clawhub.ai/user/wxd9199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers working on NVIDIA Jetson systems use this skill to inspect local CUDA Toolkit availability and NVIDIA GPU state before debugging or configuring CUDA workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local NVIDIA/CUDA diagnostic commands can reveal driver, GPU, and process information from the host. <br>
Mitigation: Use the skill only on Jetson systems where local CUDA and GPU state inspection is intended. <br>
Risk: The skill reports missing CUDA or NVIDIA tooling but does not install or configure those dependencies. <br>
Mitigation: Confirm CUDA Toolkit and nvidia-smi are installed before relying on the diagnostic output. <br>


## Reference(s): <br>
- [Jetson CUDA on ClawHub](https://clawhub.ai/wxd9199/jetson-cuda) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CUDA Toolkit and NVIDIA tools to be installed on the target Jetson system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
