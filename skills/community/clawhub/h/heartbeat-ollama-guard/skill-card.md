## Description:

Switches OpenClaw heartbeat configuration to a local Ollama model and deploys a local guard that reverts unauthorized heartbeat model changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to reduce paid cloud token usage from heartbeat calls by configuring a local Ollama model and monitoring heartbeat settings for unauthorized changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installs an always-running local guard that can overwrite OpenClaw heartbeat configuration.

Mitigation: Install only when that behavior is intended, review generated guard files and configuration before use, and use --uninstall when the service is no longer needed.

Risk: Setup guidance includes curl piped to sh for Ollama installation.

Mitigation: Prefer safer Ollama installation methods or review installation scripts before execution.

Risk: Guard configuration determines which heartbeat values are treated as authorized.

Mitigation: Keep heartbeat-guard.conf.json writable only by the intended user and review expected values before changing OpenClaw configuration.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/halfmoon82/skills/heartbeat-ollama-guard)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python-based local configuration actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, it can produce local OpenClaw configuration changes, backups, a guard daemon script, and LaunchAgent or systemd service files.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, clawhub.yaml, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
