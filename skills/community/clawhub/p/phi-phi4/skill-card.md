## Description:

Phi Phi4 helps agents guide setup and use of Microsoft Phi models through an Ollama Herd local fleet on macOS, Linux, and Windows devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and run Phi-family local model workflows with Ollama Herd, including router startup, fleet node setup, OpenAI-compatible API calls, and fleet monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned external package may run code that has not been reviewed for the deployment environment.

Mitigation: Install ollama-herd only from a trusted publisher source, preferably in a virtual environment and with a pinned reviewed version.

Risk: The local router exposes localhost APIs and uses fleet state and log files under ~/.fleet-manager.

Mitigation: Run the fleet only in trusted local environments, avoid sensitive prompts or audio unless the fleet setup is approved, and monitor the documented state and log paths.

Risk: Model downloads and deletion operations can consume storage or remove local assets.

Mitigation: Require explicit user confirmation for model pulls and deletions, consistent with the skill guardrails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/phi-phi4)
- [Ollama Herd Project](https://github.com/geeks-accelerator/ollama-herd)
- [Ollama Herd Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Ollama Herd API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [ollama-herd on PyPI](https://pypi.org/project/ollama-herd/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash, Python, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides local service endpoints, model names, hardware guidance, and guardrails for user-confirmed model operations.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
