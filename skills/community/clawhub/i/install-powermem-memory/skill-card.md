## Description:

Step-by-step guide to install and configure the PowerMem long-term memory plugin (full path, options, troubleshooting). After setup, the plugin auto-captures conversation highlights and auto-recalls relevant memories. This skill is self-contained and can be published independently of any minimal-install skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teingi](https://clawhub.ai/user/teingi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, verify, and troubleshoot PowerMem as an OpenClaw long-term memory plugin. It supports local CLI/SQLite setups and optional HTTP server deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTTP setup can expose persistent conversation memory on all network interfaces when run on 0.0.0.0 with optional authentication.

Mitigation: Prefer local CLI/SQLite mode, or place the HTTP server behind strong authentication and network restrictions.

Risk: Auto-capture can store secrets, regulated data, or other sensitive conversation content.

Mitigation: Disable autoCapture when handling secrets or regulated data, and review memory contents and retention settings before deployment.

Risk: Unverified package or plugin versions can create supply-chain or compatibility risk during installation.

Mitigation: Use a virtual environment and pin or verify the PowerMem package and plugin versions before installing.

## Reference(s):

- [PowerMem GitHub Repository](https://github.com/oceanbase/powermem)
- [PowerMem Environment Example](https://github.com/oceanbase/powermem/blob/master/.env.example)
- [PowerMem Issues](https://github.com/oceanbase/powermem/issues)
- [memory-powermem Installation Guide](https://github.com/ob-labs/memory-powermem/blob/main/INSTALL.md)
- [ClawHub Skill Page](https://clawhub.ai/teingi/skills/install-powermem-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation order, CLI and HTTP mode configuration, verification commands, and troubleshooting guidance.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
