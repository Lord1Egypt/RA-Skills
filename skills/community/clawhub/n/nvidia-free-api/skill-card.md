## Description:

Guides developers in configuring NVIDIA's OpenAI-compatible API with OpenClaw and the Python OpenAI SDK for model listing, chat, streaming, and embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure NVIDIA's OpenAI-compatible API endpoint, set their own NVIDIA API key, and try supported chat, streaming, embedding, and model-selection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may place NVIDIA API keys in shell profiles or provider configuration files.

Mitigation: Use a personal NVIDIA API key, avoid committing secrets, and review local configuration changes before saving provider settings or environment-variable exports.

Risk: The artifact documentation is Chinese-only, which may make setup details easier to misunderstand for some users.

Mitigation: Review the configuration examples carefully and confirm endpoint, model, and API-key settings before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/nvidia-free-api)
- [NVIDIA API catalog](https://build.nvidia.com/)
- [NVIDIA OpenAI-compatible API endpoint](https://integrate.api.nvidia.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, Python, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-supplied NVIDIA_API_KEY values and OpenAI-compatible provider configuration examples.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
