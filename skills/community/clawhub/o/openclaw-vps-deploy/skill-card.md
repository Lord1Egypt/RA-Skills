## Description: <br>
Deploy a custom OpenClaw repo, official package, or fork to a Hostinger VPS and make it reachable as a cloud-hosted OpenClaw service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to provision an OpenClaw gateway on a remote VPS, including SSH setup, Node.js installation, OpenClaw installation, systemd service configuration, firewall changes, and auth token generation. It also supports multi-agent VPS layouts with separate ports, workspaces, services, and optional Cloudflare tunnel exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment can create a persistent, internet-reachable root service and open a gateway port on the VPS. <br>
Mitigation: Keep the gateway behind HTTPS, VPN, or a trusted tunnel where possible, close public ports when not needed, and disable the service after use if persistence is unnecessary. <br>
Risk: The workflow handles SSH trust, private keys, model-provider API keys, and generated auth tokens. <br>
Mitigation: Verify the VPS SSH fingerprint, avoid storing private keys in temporary paths, use dedicated low-blast-radius API keys, and protect and rotate generated tokens. <br>
Risk: Custom repository or package values are installed and built on the target VPS. <br>
Mitigation: Use only trusted repository and package inputs and review deployment settings before running the script. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/openclaw-vps-deploy) <br>
- [OpenClaw VPS Deploy Skill](SKILL.md) <br>
- [Known Gotchas - OpenClaw VPS Deployment](references/gotchas.md) <br>
- [Multi-Agent VPS Deployment](references/multi-agent.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, JSON, Python, and systemd configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment commands that handle SSH access, API keys, firewall state, persistent services, and auth tokens.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
