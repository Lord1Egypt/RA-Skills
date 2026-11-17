## Description:

Infinity Router routes AI requests across free OpenRouter chat models for OpenClaw and Claude Code by auto-discovering, scoring, and configuring a primary model with fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genoshide](https://clawhub.ai/user/genoshide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use Infinity Router to configure OpenClaw or Claude Code with ranked free OpenRouter chat models and fallback chains for model switching, rate-limit handling, and AI cost reduction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can overwrite globally available infinity-router commands.

Mitigation: Prefer pipx or a user-local bin directory, avoid running the installer as root, and check for existing infinity-router commands before installing.

Risk: The skill uses OpenRouter API keys and writes AI-tool configuration.

Mitigation: Protect OpenRouter keys as secrets and review OpenClaw or Claude Code configuration changes before applying them.

Risk: Watcher and webhook modes can automatically change model configuration and restart the gateway.

Mitigation: Enable watch or webhook behavior only when automatic rotation and restarts are intended, and use validation before writing model choices.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/genoshide/skills/infinity-router)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify OpenClaw and Claude Code model configuration when installed and executed.]

## Skill Version(s):

2.1.0 (source: release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
