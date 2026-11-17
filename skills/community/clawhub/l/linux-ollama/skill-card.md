## Description:

Linux Ollama helps agents set up and operate an Ollama fleet router across Linux servers, desktops, and edge devices with load balancing, systemd services, monitoring, and OpenAI-compatible access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Ollama Herd across Linux machines, expose a shared router endpoint, manage systemd services, and monitor fleet health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to run mutable installers for Ollama and ollama-herd.

Mitigation: Audit installers before execution and pin package versions where possible.

Risk: The skill creates persistent systemd services for the router and node agent.

Mitigation: Run services under a dedicated unprivileged account and review service files before enabling them.

Risk: The router and dashboard use port 11435 and could expose fleet controls if reachable from untrusted networks.

Mitigation: Restrict port 11435 to trusted private hosts or a protected network; do not expose it publicly without authentication and TLS.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/linux-ollama)
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, Python, JSON, and systemd configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installer commands, service definitions, firewall rules, API examples, monitoring commands, and guardrails for model downloads and deletion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
