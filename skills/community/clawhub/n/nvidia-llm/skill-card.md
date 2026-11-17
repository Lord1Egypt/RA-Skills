## Description:

Routes chat and streaming prompts across NVIDIA-compatible NIM model endpoints with automatic fallback, circuit breaking, latency tracking, and subscription-gated CLI/library access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Python and CLI access to routed LLM chat, streaming, model selection, and health checks across multiple NVIDIA-compatible model endpoints. It is intended for general, code, reasoning, translation, finance, medical, multimodal, and low-latency routing scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to NVIDIA-compatible remote model endpoints, and hedged routing can send the same prompt to more than one model endpoint.

Mitigation: Use the skill only with data approved for those endpoints, avoid secrets or regulated data in prompts, and disable or avoid hedged routing where single-endpoint handling is required.

Risk: Credential and request behavior depends on the configured NVIDIA_API_KEY and base_url.

Mitigation: Set your own NVIDIA_API_KEY, review any custom base_url before use, and do not rely on untrusted endpoint configuration.

Risk: The skill writes local license and usage state under the user's home directory.

Mitigation: Review the local state files and install only in environments where per-user license and usage tracking is acceptable.

Risk: The WeChat subscription path is a third-party payment arrangement outside the platform.

Mitigation: Verify the publisher, payment terms, and activation process before making payment or entering activation codes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjkj999999/skills/nvidia-llm)
- [NVIDIA-compatible API base endpoint](https://integrate.api.nvidia.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, Python snippets, CLI commands, and JSON-like status/result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream text chunks and return selected model alias, latency, and usage metadata for API calls.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
