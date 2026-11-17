## Description:

Installs and operates KeepGPU for GPU keep-alive workflows, including command construction, blocking and service modes, status checks, tuning, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangmerlyn](https://clawhub.ai/user/wangmerlyn)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build run-ready KeepGPU installation and operation command sequences for keeping accessible GPUs active during workloads, with verification, stop, and cleanup steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background KeepGPU sessions can reserve GPU memory or otherwise affect shared compute resources.

Mitigation: Confirm the machine policy allows GPU reservation, choose the smallest useful VRAM setting, and verify cleanup with keep-gpu status, keep-gpu stop, and keep-gpu service-stop.

Risk: Installation or long-running service commands can affect the user's Python environment or leave keep-alive processes running.

Mitigation: Install only from trusted sources, preferably in a virtual environment with pinned versions or reviewed commits, and include explicit verification and stop commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangmerlyn/skills/gpu-keepalive-with-keepgpu)
- [KeepGPU Git install source referenced by the skill](https://github.com/Wangmerlyn/KeepGPU.git)
- [PyTorch CUDA wheel index referenced by the skill](https://download.pytorch.org/whl/cu121)
- [PyTorch ROCm wheel index referenced by the skill](https://download.pytorch.org/whl/rocm6.1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
