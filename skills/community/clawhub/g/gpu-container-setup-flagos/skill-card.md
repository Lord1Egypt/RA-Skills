## Description: <br>
Automatically detects GPU vendor, finds an appropriate PyTorch container image, launches it with vendor-specific mounts, and validates GPU functionality for NVIDIA, Ascend, Metax, Iluvatar, and AMD/ROCm systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up PyTorch GPU containers across supported vendors by detecting hardware, selecting or testing a container image, mounting required devices and data paths, and validating PyTorch GPU access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can pull and run GPU container images and mount host GPU devices and data paths. <br>
Mitigation: Supervise proposed Docker commands, prefer explicit trusted image names or known vendor registries, and confirm mounts expose only the intended host paths. <br>
Risk: The skill may try to update its own image-source reference file after discovering a working registry through web search. <br>
Mitigation: Review and approve any proposed edits to reference files before allowing the skill to persist new registry guidance. <br>
Risk: Vendor-specific mounts and security flags can expose host drivers, devices, or data to a container. <br>
Mitigation: Use read-only driver mounts where possible, avoid broad privileges unless required, and validate container behavior before using it for workloads. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wbavon/gpu-container-setup-flagos) <br>
- [GPU Vendor Detection Methods](references/gpu-detection.md) <br>
- [Container Image Discovery Guide](references/image-sources.md) <br>
- [Vendor-Specific Mount Requirements](references/mount-requirements.md) <br>
- [NVIDIA NGC PyTorch tags API](https://api.ngc.nvidia.com/v2/repos/nvidia/pytorch/tags) <br>
- [Ascend Hub PyTorch model zoo](https://ascendhub.huawei.com/public-ascendhub/pytorch-modelzoo) <br>
- [Docker Hub ROCm PyTorch tags API](https://hub.docker.com/v2/repositories/rocm/pytorch/tags) <br>
- [BAAI Harbor flagrelease-public API](https://harbor.baai.ac.cn/api/v2.0/projects/flagrelease-public/repositories?page_size=100) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON snippets and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker commands, selected image names, mount paths, detected GPU details, validation results, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
