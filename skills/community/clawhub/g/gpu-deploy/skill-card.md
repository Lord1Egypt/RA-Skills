## Description:

Deploys vLLM model services on GPU servers with multi-server configuration, GPU and port checks, preset open-source model choices, and service management commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT License

## Use Case:

Developers and ML infrastructure engineers use this skill to configure GPU hosts, check resource availability, and deploy or manage vLLM model services over SSH.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote deployment or stop commands can affect workloads on configured GPU hosts.

Mitigation: Confirm the SSH target, selected server, model path, port, and active workloads before running deployment or stop commands.

Risk: A vLLM service port may be exposed or conflict with another service.

Mitigation: Check port availability and firewall exposure before starting the model service.

## Reference(s):

- [vLLM Project](https://github.com/vllm-project/vllm)
- [vLLM Documentation](https://docs.vllm.ai)
- [Hugging Face Models](https://huggingface.co/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose SSH-based deployment and service management commands for user-controlled GPU hosts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
