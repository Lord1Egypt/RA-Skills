## Description:

Manages free AI models from OpenRouter for OpenClaw by ranking available models, configuring fallbacks for rate-limit handling, and updating OpenClaw model configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pz33y](https://clawhub.ai/user/pz33y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to reduce model costs by selecting OpenRouter free models, setting a primary model, and maintaining fallback models when rate limits occur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can expose the OpenRouter API key if the key is echoed or stored in shared files.

Mitigation: Use a presence-only API key check, avoid printing secrets, and keep OPENROUTER_API_KEY out of files that may be shared.

Risk: The skill persistently changes OpenClaw model configuration.

Mitigation: Back up ~/.openclaw/openclaw.json before running configuration-changing commands and review the resulting model and fallback settings.

Risk: Installation and runtime behavior depend on an external Python dependency and OpenRouter service availability.

Mitigation: Prefer a pinned installer/dependency set and review availability or rate-limit failures before relying on the configured fallback chain.

## Reference(s):

- [SEEK on ClawHub](https://clawhub.ai/pz33y/skills/nmvnb)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenRouter API models endpoint](https://openrouter.ai/api/v1/models)
- [OpenRouter API keys](https://openrouter.ai/keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include OpenClaw configuration changes and OpenRouter API checks that require OPENROUTER_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
