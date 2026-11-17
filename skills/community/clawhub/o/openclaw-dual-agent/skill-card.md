## Description:

Run two OpenClaw agents simultaneously: a paid Anthropic agent and a free agent using OpenRouter or local Ollama models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure two concurrent OpenClaw agents with separate Telegram bot routing and either OpenRouter or local Ollama model backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot tokens and API keys can be exposed if copied directly into shell commands or shared logs.

Mitigation: Use interactive onboarding or environment variables, redact tokens before sharing logs, and set auth-profiles.json and openclaw.json to mode 600.

Risk: Hybrid Ollama configurations can route prompts or context to OpenRouter cloud through fallback or heartbeat settings.

Mitigation: Remove OpenRouter fallback and heartbeat model references when fully local Ollama-only operation is required.

## Reference(s):

- [OpenClaw Dual Agent on ClawHub](https://clawhub.ai/djc00p/skills/openclaw-dual-agent)
- [Configuration Reference](artifact/references/config-reference.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for configuring OpenClaw agents, Telegram routing, model providers, and local or cloud fallback behavior.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
