## Description: <br>
Deploys vLLM-based LLM services on GPU servers with multi-server configuration, GPU and port checks, and presets for popular open-source models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure GPU servers, check resource and port availability, deploy vLLM model services, inspect running services, and stop deployments when no longer needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands operate over SSH against GPU servers and can affect remote services or shared compute resources. <br>
Mitigation: Verify the SSH host, account, model path, GPU availability, and target port before deployment, and run the documented check command first. <br>
Risk: A vLLM service may continue running in a tmux session after deployment. <br>
Mitigation: Monitor the service after launch, inspect running processes, and stop the service when it is no longer needed. <br>
Risk: Untested configuration on production servers can cause resource contention or service disruption. <br>
Mitigation: Test deployments in a non-production environment before using production GPU hosts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wang-junjian/llm-deploy) <br>
- [vLLM Project](https://github.com/vllm-project/vllm) <br>
- [vLLM Documentation](https://docs.vllm.ai) <br>
- [Hugging Face Models](https://huggingface.co/models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SSH access to the target GPU server and user-supplied server, model path, and port configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
