## Description: <br>
Deploy MiniCPM-o 4.5 multimodal services with guidance for Web Demo setup, model download and verification, HTTPS configuration, service startup, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZMXJJ](https://clawhub.ai/user/ZMXJJ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, configure, start, and troubleshoot MiniCPM-o 4.5 services on supported NVIDIA GPU systems. It helps select the supported Web Demo path, prepare the environment, verify model files, configure HTTPS access, and diagnose startup issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment commands install packages, clone third-party code, and download large model files. <br>
Mitigation: Use a fresh virtual environment, container, or dedicated machine, and review the cloned repository and install script before running them. <br>
Risk: Some setup examples use sudo for system package installation. <br>
Mitigation: Avoid sudo unless you accept system package changes and have reviewed the exact package operations. <br>
Risk: Self-signed certificate examples may train users to bypass browser certificate warnings. <br>
Mitigation: Treat certificate bypass examples as localhost-only testing guidance and replace self-signed certificates with proper certificates for shared or production access. <br>
Risk: Unsupported devices or deployment paths may fail or produce misleading troubleshooting paths. <br>
Mitigation: Follow the artifact's support boundary: use Web Demo on NVIDIA GPUs with at least 12 GB VRAM, and do not guide unsupported vLLM, llamacpp-omni, CPU-only, Apple Silicon, AMD, Intel Arc, Ascend NPU, or low-VRAM deployments. <br>


## Reference(s): <br>
- [MiniCPM-o Documentation](https://minicpm-o.readthedocs.io/) <br>
- [MiniCPM-o 4.5 Hugging Face Model](https://huggingface.co/openbmb/MiniCPM-o-4_5) <br>
- [MiniCPM-o 4.5 AWQ Hugging Face Model](https://huggingface.co/openbmb/MiniCPM-o-4_5-awq) <br>
- [MiniCPM-o 4.5 ModelScope Model](https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5) <br>
- [MiniCPM-o Demo Repository](https://github.com/OpenBMB/MiniCPM-o-Demo.git) <br>
- [Web Demo Deployment Reference](references/web-demo-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and Python utility usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance only; commands should be reviewed before execution in the user's environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
