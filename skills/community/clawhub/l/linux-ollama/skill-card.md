## Description: <br>
Linux Ollama guides agents through setting up and operating Ollama Herd for multi-machine Ollama routing on Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Linux Ollama fleets, expose a local router, manage systemd services, and monitor health and logs for local inference workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to expose a persistent Ollama router service on port 11435. <br>
Mitigation: Bind or firewall the service to trusted hosts only, and use subnet restrictions, VPN, authentication, and TLS before allowing broader network access. <br>
Risk: The setup flow includes network-sourced installation commands. <br>
Mitigation: Review installers before execution where possible and prefer pinned or verified packages from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/linux-ollama) <br>
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JSON, and systemd configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Linux-focused setup guidance; requires curl or wget, with optional python3, pip, nvidia-smi, and systemctl.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
