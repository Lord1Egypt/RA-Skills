## Description: <br>
Install and operate KeepGPU for GPU keep-alive with both blocking CLI and non-blocking service workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wangmerlyn](https://clawhub.ai/user/Wangmerlyn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install KeepGPU and generate safe keep-gpu command sequences for blocking or service-mode GPU keep-alive sessions, including status checks, stop commands, dashboard access, tuning, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing external packages or Git-based dependencies can introduce unreviewed code into the runtime environment. <br>
Mitigation: Trust the KeepGPU package source before installing, prefer a virtual environment, and use pinned or reviewed versions where possible. <br>
Risk: GPU keep-alive sessions can consume VRAM or interfere with other workloads on shared machines. <br>
Mitigation: Specify GPU IDs, choose conservative VRAM settings, respect cluster policy, and stop the service or background process when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wangmerlyn/gpu-keepalive-with-keepgpu) <br>
- [KeepGPU repository](https://github.com/Wangmerlyn/KeepGPU.git) <br>
- [PyTorch CUDA wheels](https://download.pytorch.org/whl/cu121) <br>
- [PyTorch ROCm wheels](https://download.pytorch.org/whl/rocm6.1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation commands, GPU selection, VRAM and interval settings, verification steps, stop commands, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
