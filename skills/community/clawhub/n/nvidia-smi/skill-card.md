## Description:

Provides detailed guidance on using the nvidia-smi command for real-time NVIDIA GPU monitoring, management, troubleshooting, and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duanc-chao](https://clawhub.ai/user/duanc-chao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, machine learning engineers, and system administrators use this skill to interpret nvidia-smi output, monitor NVIDIA GPU health and utilization, diagnose CUDA out-of-memory issues, and create monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminating GPU processes can interrupt active workloads or shared jobs.

Mitigation: Confirm the PID, owner, and workload impact first; prefer scheduler-native cancellation or graceful shutdown on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duanc-chao/skills/nvidia-smi)
- [Publisher profile](https://clawhub.ai/user/duanc-chao)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with inline shell commands and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes GPU monitoring, troubleshooting, and automation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
