## Description:

OpenClaw Doc Finder helps agents route OpenClaw configuration, CLI, channel, provider, and troubleshooting questions to official documentation with precise URLs, commands, and configuration snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mslclaw](https://clawhub.ai/user/mslclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer OpenClaw setup, configuration, command, provider, channel, and troubleshooting questions from official documentation. It is intended to return targeted documentation links plus actionable command and configuration examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote fetch, curl fallback, cache writes, lookup-record writes, and version-sync runs may retrieve untrusted content or persist local changes.

Mitigation: Require explicit user approval before web fetches, curl commands, cache writes, lookup-record writes, or version synchronization.

Risk: Troubleshooting commands and configuration examples may expose credentials, environment variables, API keys, gateway tokens, or sensitive logs.

Mitigation: Redact secrets before presenting command output and avoid printing raw .env files, API keys, gateway tokens, or full sensitive logs into chat.

Risk: Suggested gateway host changes or unpinned install fallbacks can weaken deployment security.

Mitigation: Avoid unpinned install fallbacks unless the source is pinned and verified, and do not expose the gateway on 0.0.0.0 without private-network controls, authentication, and firewall restrictions.

## Reference(s):

- [OpenClaw Doc Finder ClawHub page](https://clawhub.ai/mslclaw/skills/openclaw-doc-finder)
- [OpenClaw documentation index](references/doc-index.md)
- [Gateway configuration guide snippets](references/config-guide.md)
- [OpenClaw diagnostic decision tree](references/diagnostic-tree.md)
- [OpenClaw troubleshooting snippets](references/troubleshoot.md)
- [OpenClaw documentation lookup history](references/doc-lookups.md)
- [Gateway configuration examples](https://docs.openclaw.ai/gateway/configuration-examples)
- [Channel troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)
- [Secrets management](https://docs.openclaw.ai/gateway/secrets)
- [Remote gateway](https://docs.openclaw.ai/gateway/remote)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with official documentation URLs, bash code blocks, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes version notes and manual documentation links when automated retrieval is unavailable.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
