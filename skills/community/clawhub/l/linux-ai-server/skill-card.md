## Description: <br>
Linux AI Server turns Linux servers into a local AI inference cluster for headless operation with systemd, NVIDIA CUDA, and no GUI overhead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Linux server administrators use this skill to set up and operate headless local AI inference servers and route requests across a small fleet. It provides install, systemd, firewall, monitoring, and API usage guidance for Linux-based Ollama Herd deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The router API and dashboard can expose local inference capabilities on port 11435 if reachable from untrusted networks. <br>
Mitigation: Bind to localhost or a private network, restrict firewall sources, and use VPN, SSH tunneling, or an authenticated TLS proxy for remote access. <br>
Risk: The setup flow relies on a remote install script and a PyPI package that change the server environment. <br>
Mitigation: Review the install script and package before use, and test deployment on a noncritical machine before production rollout. <br>
Risk: Model downloads and deletions can consume resources or remove local assets if performed accidentally. <br>
Mitigation: Keep explicit confirmation for model downloads and deletions, and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/linux-ai-server) <br>
- [Ollama Herd Project](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, JSON, and systemd configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Linux-only setup guidance, OpenAI-compatible API examples, monitoring endpoints, firewall commands, and model-operation guardrails.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
