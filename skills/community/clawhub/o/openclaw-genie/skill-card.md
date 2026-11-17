## Description:

Helps agents answer questions about OpenClaw installation, configuration, agents, channels, memory, tools, deployment, Docker, OAuth, browser, PDF, voice, secrets, sandboxing, automation, and messaging integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fcsouza](https://clawhub.ai/user/fcsouza)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to get grounded OpenClaw setup, configuration, deployment, and operational guidance, including commands and JSON examples for channels, tools, memory, multi-agent routing, and security-related settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable install commands can execute remote scripts or install mutable latest packages.

Mitigation: Review install commands first and prefer pinned package versions or verified release artifacts.

Risk: Deployment guidance can enable daemons, gateway services, or system-wide services with broad local impact.

Mitigation: Avoid running setup as root unless required, and review service scope, bind address, and authentication before enabling services.

Risk: Messaging tokens, OAuth credentials, and gateway tokens may be exposed through configuration examples.

Mitigation: Store credentials in environment variables or secret references and audit token coverage before deployment.

Risk: Browser private-network access, native PDF uploads, memory/session indexing, and companion device features can expand privacy and network exposure.

Mitigation: Enable these features deliberately, use sandboxing and allowlists where available, and review data retention settings.

## Reference(s):

- [OpenClaw Configuration Reference](references/configuration.md)
- [OpenClaw Channels Reference](references/channels.md)
- [OpenClaw Memory System Reference](references/memory.md)
- [OpenClaw Tools Reference](references/tools.md)
- [OpenClaw Deployment Reference](references/deployment.md)
- [OpenClaw Multi-Agent Reference](references/multi-agent.md)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/fcsouza/skills/openclaw-genie)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or JSONC configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory content for an agent; commands and configuration changes require user review before execution.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
