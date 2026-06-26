## Description: <br>
Helps deploy vLLM model services on GPU servers, including multi-server configuration, GPU and port checks, and one-command deployment for popular open-source models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to prepare GPU server configuration, check GPU and port availability over SSH, and generate deployment commands for vLLM model services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run SSH commands against GPU servers, which may affect remote services or expose operational resources if targets are wrong. <br>
Mitigation: Use trusted hosts, least-privileged SSH accounts where possible, and confirm host, port, and model targets before executing commands. <br>
Risk: The release does not include executable code, so behavior depends on any external gpu-deploy script placed on the user's PATH. <br>
Mitigation: Review the external gpu-deploy script before installation or use the documented manual SSH commands directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wang-junjian/gpu-deploy) <br>
- [vLLM documentation](https://docs.vllm.ai) <br>
- [vLLM project](https://github.com/vllm-project/vllm) <br>
- [Hugging Face models](https://huggingface.co/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SSH access to target GPU servers and a trusted gpu-deploy command or equivalent manual commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
