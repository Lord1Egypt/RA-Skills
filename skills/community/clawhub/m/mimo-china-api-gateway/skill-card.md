## Description:

中国AI API统一网关 helps developers compare China-based AI API providers and configure OpenAI-compatible routing, load balancing, and fallback examples for MiMo, DeepSeek, Qwen, GLM, and related services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select low-cost or free China-based AI APIs, obtain provider setup guidance, and generate OpenAI-compatible API calls, gateway configuration, and troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included gateway code can expose provider accounts if deployed as a public unauthenticated service.

Mitigation: Bind the service locally unless explicitly hardened, and add authentication, authorization, rate limits, request size limits, and quota controls before network exposure.

Risk: Provider API keys may be leaked or misused if stored directly in configuration files.

Mitigation: Store real provider keys in environment variables or a secret manager, and avoid committing populated YAML configuration files.

Risk: Prompts, code, and other request payloads may be sent to third-party AI providers through the gateway examples.

Mitigation: Review provider terms and data handling requirements before sending sensitive or regulated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-china-api-gateway)
- [中国AI API统一网关 - 详细内容](references/details.md)
- [中国AI平台注册与API获取指南](references/platforms.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Python, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider comparison guidance, API key setup steps, gateway configuration examples, and OpenAI-compatible request snippets.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
