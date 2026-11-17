## Description:

Deploys vLLM-based large language model services on GPU servers, with guidance for multi-server configuration, GPU and port checks, and common open-source model deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure remote GPU servers and deploy or manage vLLM model services over SSH.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can start long-running model services on remote GPU servers over SSH.

Mitigation: Review the target server, user, model path, GPU allocation, and port before running deployment commands.

Risk: Example model aliases and service names may not match the underlying model being deployed.

Mitigation: Confirm served model names and aliases before exposing the service to users or dependent applications.

Risk: The documentation is primarily in Chinese, which may lead to misconfiguration for readers who are not comfortable with it.

Mitigation: Have an operator who understands the documentation review configuration and command choices before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wang-junjian/skills/llm-deploy)
- [vLLM Documentation](https://docs.vllm.ai)
- [vLLM Project](https://github.com/vllm-project/vllm)
- [Hugging Face Models](https://huggingface.co/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; commands target remote GPU servers over SSH.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
