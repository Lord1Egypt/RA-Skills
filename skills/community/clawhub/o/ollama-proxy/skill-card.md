## Description: <br>
Ollama proxy - one endpoint that routes to multiple Ollama instances as a drop-in Ollama API replacement for localhost:11434, with automatic node discovery, routing, scoring, and retry behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure agents and applications to route Ollama-compatible chat, generation, model, and OpenAI-compatible API requests through an Ollama proxy across trusted local Ollama nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The proxy and dashboard are intended for a trusted LAN or VPN; public exposure could reveal traffic patterns or operational details. <br>
Mitigation: Deploy only on trusted networks, avoid public internet exposure, and review request traces stored under ~/.fleet-manager before use. <br>
Risk: The setup flow installs and runs the ollama-herd package from PyPI. <br>
Mitigation: Pin or review the package version before installation in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/ollama-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and integration instructions for a local Ollama proxy; it does not itself run the proxy.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
