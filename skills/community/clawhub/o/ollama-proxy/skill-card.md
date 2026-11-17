## Description:

Ollama Proxy provides guidance for installing and using a local-network proxy that routes Ollama API requests across multiple Ollama instances with discovery, scoring, and retry behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a drop-in Ollama proxy endpoint for multi-machine local Ollama fleets, including setup commands, compatible client configuration, and monitoring requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes prompts through a proxy host and local network, so untrusted hosts or networks could expose prompts or responses.

Mitigation: Only route prompts through a proxy host and local network you trust, as stated in the server security guidance.

Risk: The documented workflow installs and runs the third-party ollama-herd package.

Mitigation: Review the ollama-herd package or source before production use and install it in a virtual environment or container when possible.

Risk: The proxy stores latency and request-tracing data under ~/.fleet-manager.

Mitigation: Review local storage behavior before deployment and avoid deleting or modifying ~/.fleet-manager files manually.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/ollama-proxy)
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd)
- [PyPI: ollama-herd](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with bash, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local-network endpoint URLs and commands; no credential environment variables are disclosed.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
