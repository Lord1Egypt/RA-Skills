## Description:

ModelPool (Free) helps OpenClaw users discover and configure free OpenRouter models, rotate multiple API keys, build fallback chains, and run diagnostics and repair commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meilihulee](https://clawhub.ai/user/meilihulee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers using OpenClaw use this skill to set up and maintain OpenRouter-backed free model configurations, API-key rotation, fallback model chains, status checks, and repair commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses OpenRouter API keys while managing local OpenClaw configuration.

Mitigation: Verify the package name and source before installing, rotate keys that were previously passed on a command line, and check permissions on `~/.openclaw`.

Risk: `modelpool setup`, `modelpool auto`, and related commands can rewrite OpenClaw model configuration and restart OpenClaw.

Mitigation: Review configuration changes before use, keep backups of existing OpenClaw settings, and run the commands only in an environment where OpenClaw restarts are acceptable.

Risk: `modelpool repair` tests configured provider URLs, changes local state, cleans sessions or logs, and restarts OpenClaw.

Mitigation: Run repair only after confirming that automated diagnostics and local cleanup are appropriate for the target system.

## Reference(s):

- [ModelPool (Free) ClawHub page](https://clawhub.ai/meilihulee/skills/modelpool-free)
- [OpenRouter](https://openrouter.ai)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [OpenRouter API Key Guide](docs/openrouter-guide.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw configuration, store OpenRouter API keys, query provider APIs, and restart OpenClaw when commands are executed.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence and setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
