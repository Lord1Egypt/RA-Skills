## Description: <br>
Provides detailed guidance on using the nvidia-smi command for real-time NVIDIA GPU monitoring, management, troubleshooting, and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DuanC-Chao](https://clawhub.ai/user/DuanC-Chao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, system administrators, and machine learning engineers use this skill to interpret nvidia-smi output, monitor NVIDIA GPU health and utilization, diagnose CUDA memory issues, and build simple monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process termination guidance can disrupt shared GPU workloads if the wrong PID is stopped. <br>
Mitigation: Verify the PID with nvidia-smi and ps, prefer graceful shutdown, and ask an administrator before stopping another user's job. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/DuanC-Chao/nvidia-smi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for nvidia-smi monitoring, targeted queries, process inspection, daemon mode, and pynvml-based automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
