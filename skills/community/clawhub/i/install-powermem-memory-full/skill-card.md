## Description:

Step-by-step guide to install and configure the PowerMem long-term memory plugin, including setup paths, options, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teingi](https://clawhub.ai/user/teingi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install PowerMem, configure CLI or HTTP memory modes, verify long-term memory health, and troubleshoot common setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content may be stored persistently and later reinserted into prompts.

Mitigation: Use the skill only with data appropriate for long-term memory, avoid secrets or regulated data, and review auto-capture settings before enabling the plugin.

Risk: HTTP server mode can be configured to listen on all network interfaces without requiring authentication.

Mitigation: Prefer local CLI mode or bind HTTP mode to localhost; for shared deployments require authentication, TLS, and network allowlisting.

Risk: Remote installer and package installation steps may execute code from external sources.

Mitigation: Review installer contents before running them and consider pinning package versions in managed environments.

## Reference(s):

- [PowerMem Introduction](artifact/powermem-intro.md)
- [Config & Commands Quick Reference](artifact/config-reference.md)
- [memory-powermem INSTALL.md](https://github.com/ob-labs/memory-powermem/blob/main/INSTALL.md)
- [PowerMem GitHub Repository](https://github.com/oceanbase/powermem)
- [PowerMem .env Example](https://github.com/oceanbase/powermem/blob/master/.env.example)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration keys]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI and HTTP setup paths, verification commands, and troubleshooting notes.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
