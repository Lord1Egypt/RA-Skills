## Description:

Use this skill when users request to deploy LLMs such as Qwen and DeepSeek on specified GPU servers, download models with ModelScope, and start a vLLM inference service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwei1237](https://clawhub.ai/user/wangwei1237)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to deploy supported large language models on GPU servers, configure model storage, port, proxy, and tensor parallelism settings, and validate that the vLLM chat completions endpoint is running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over a remote GPU server through SSH deployment commands.

Mitigation: Use only trusted target hosts and a dedicated least-privilege SSH account, and review commands before execution.

Risk: Unvalidated model, path, proxy, port, and GPU parameters can cause incorrect downloads, unsafe paths, or unintended service exposure.

Mitigation: Validate model and path parameters, review proxy and port settings, and apply firewall or authentication controls for the vLLM API.

Risk: The deployment installs or upgrades runtime dependencies and starts the vLLM API on all interfaces as shipped.

Mitigation: Pin dependencies where practical and avoid public exposure unless network access controls and authentication are in place.

## Reference(s):

- [ClawHub Model Deploy Skill](https://clawhub.ai/wangwei1237/skills/model-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces remote deployment steps and validation commands for user-specified model and GPU server parameters.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
