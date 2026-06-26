## Description: <br>
Llama 3 by Meta helps agents run Llama 3.3, Llama 3.2, and Llama 3.1 across a local device fleet with an OpenAI-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate a local Ollama fleet router for Llama-family models, route requests to available devices, and inspect fleet health and model availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an unpinned third-party local AI router and node agent. <br>
Mitigation: Review the ollama-herd package and source before installation, pin an approved version, and run it only on trusted devices. <br>
Risk: The router may expose local model services and telemetry-like features across a machine or network. <br>
Mitigation: Restrict service binding to localhost or a trusted LAN, limit firewall access, and decide whether per-app analytics, capacity learning, and meeting detection are acceptable before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/llama-llama3) <br>
- [ollama-herd project](https://github.com/geeks-accelerator/ollama-herd) <br>
- [ollama-herd PyPI package](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, Python, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local service endpoints, model names, hardware guidance, and guardrails for model downloads and file changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
