## Description:

Automatically detect GPU vendor, find an appropriate PyTorch container image, launch with correct mounts, and validate GPU functionality for NVIDIA, Ascend, Metax, Iluvatar, and AMD/ROCm systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to prepare PyTorch GPU containers across supported vendor hardware, including GPU detection, data mount selection, container image selection, Docker launch commands, and validation of GPU-backed PyTorch execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run web-discovered Docker images with host GPU devices and data mounts.

Mitigation: Review and approve each Docker image and docker run command before execution, and prefer trusted, digest-pinned, signed images.

Risk: The skill can persistently add web-discovered image sources to its trusted source list.

Mitigation: Disable or remove the web-search auto-execution and self-update path, or require manual review of source-list changes before reuse.

Risk: GPU and data mounts can expose host devices and files to container workloads.

Mitigation: Expose only the specific devices and host paths required for the workload and avoid untrusted code or images with those mounts.

## Reference(s):

- [Gpu Container Setup Flagos on ClawHub](https://clawhub.ai/wbavon/skills/gpu-container-setup-flagos)
- [GPU Vendor Detection Methods](references/gpu-detection.md)
- [Container Image Discovery Guide](references/image-sources.md)
- [Vendor-Specific Mount Requirements](references/mount-requirements.md)
- [NVIDIA NGC PyTorch Tags API](https://api.ngc.nvidia.com/v2/repos/nvidia/pytorch/tags)
- [Docker Hub ROCm PyTorch Tags API](https://hub.docker.com/v2/repositories/rocm/pytorch/tags)
- [BAAI Harbor FlagRelease Public Repositories API](https://harbor.baai.ac.cn/api/v2.0/projects/flagrelease-public/repositories?page_size=100)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Docker, GPU detection, disk inspection, image lookup, and PyTorch validation steps when invoked by an agent with the required tools and user approval.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
