## Description: <br>
Deploys LLMs such as Qwen or DeepSeek on GPU servers by downloading models from ModelScope and starting a vLLM inference service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwei1237](https://clawhub.ai/user/wangwei1237) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy large language models to GPU servers, configure the vLLM runtime, and verify that an OpenAI-compatible chat completions endpoint is running. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify GPU servers over SSH and run deployment commands on a target host. <br>
Mitigation: Use a dedicated least-privileged SSH account and confirm the target host, user, path, model, port, and command before each run. <br>
Risk: The vLLM service may be exposed beyond the local machine if started on an unrestricted network interface. <br>
Mitigation: Restrict access with localhost binding, firewall rules, reverse proxy authentication, or trusted source IP allowlists. <br>
Risk: Unpinned package installation can introduce unexpected dependency changes. <br>
Mitigation: Pin vLLM and ModelScope dependency versions in controlled deployment environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangwei1237/model-deploy) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Deployment script](artifact/scripts/deploy.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment steps and commands for SSH, conda, ModelScope, and vLLM; no structured machine-readable output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
