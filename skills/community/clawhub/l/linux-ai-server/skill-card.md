## Description:

Linux AI Server turns Linux servers into a local AI inference cluster with headless operation, systemd services, NVIDIA CUDA support, and REST/OpenAI-compatible endpoints for models such as Llama, Qwen, DeepSeek, Phi, and Mistral.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Linux server administrators use this skill for guidance on setting up and operating a headless local AI inference cluster across Linux servers, including router/node commands, systemd service configuration, firewall setup, monitoring endpoints, and client API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses remote installer and package installation commands that may change over time.

Mitigation: Review the Ollama installer and ollama-herd package provenance before running commands, and prefer pinned versions, hashes, signatures, or a dedicated virtual environment.

Risk: The router and dashboard may expose unauthenticated HTTP endpoints on the network.

Mitigation: Bind services to localhost, a VPN, or a tightly allowlisted interface unless authentication and TLS are added.

Risk: The systemd examples create always-on services.

Mitigation: Confirm how to stop, disable, and remove the services before enabling them on shared or production systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/linux-ai-server)
- [Publisher Profile](https://clawhub.ai/user/twinsgeeks)
- [Ollama Herd Project](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, JSON, and systemd configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, service definitions, API examples, hardware guidance, firewall rules, monitoring commands, and guardrails for model download and deletion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
