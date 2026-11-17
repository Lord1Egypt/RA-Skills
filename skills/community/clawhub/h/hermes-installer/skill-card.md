## Description:

Hermes Installer guides agents through installing, updating, diagnosing, and configuring Hermes Agent, including model-provider APIs and Feishu, Telegram, and Discord gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongyu23](https://clawhub.ai/user/dongyu23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install Hermes Agent, configure supported model providers, set up messaging gateways, run diagnostics, update deployments, and remove local installations when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives broad installation, update, and container commands that can execute mutable code.

Mitigation: Review commands before execution and pin the Hermes Agent repository revision and dependencies for controlled deployments.

Risk: Hermes credentials are stored under ~/.hermes and diagnostics may expose configuration or log details.

Mitigation: Protect ~/.hermes, avoid sharing raw diagnostic output, and redact API keys, tokens, base URLs, and logs before disclosure.

Risk: The diagnostic script can send configured API keys to the user-provided OPENAI_BASE_URL endpoint.

Mitigation: Run diagnostics only after verifying the endpoint is trusted and not mistyped.

Risk: Docker deployment mounts ~/.hermes into the container, exposing persistent configuration and credentials to the container runtime.

Mitigation: Use trusted images and host paths, restrict container access, and separate sensitive configuration for shared or multi-user hosts.

## Reference(s):

- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Hermes Agent repository](https://github.com/NousResearch/hermes-agent)
- [ClawHub skill page](https://clawhub.ai/dongyu23/skills/hermes-installer)
- [OpenRouter documentation](https://openrouter.ai/docs)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Discord Developer Portal](https://discord.com/developers/applications)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell, YAML, environment-variable, and PowerShell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install packages, clone repositories, build Docker images, manage gateway processes, and edit files under ~/.hermes.]

## Skill Version(s):

1.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
