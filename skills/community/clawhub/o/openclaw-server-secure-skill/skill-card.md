## Description: <br>
Comprehensive security hardening and installation guide for OpenClaw (formerly Clawdbot/Moltbot). Use this skill when the user wants to secure a server, install the OpenClaw agent, or configure Tailscale/Firewall for the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kime541200](https://clawhub.ai/user/kime541200) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and server operators use this skill to harden a self-hosted OpenClaw server, install the OpenClaw agent, configure access controls, and verify the deployment with security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides persistent server-level security changes, including SSH, firewall, VPN, package installation, and credential permission changes. <br>
Mitigation: Confirm console or out-of-band access first, verify SSH key login, review each command, and keep recoverable backups of changed configuration files. <br>
Risk: Firewall changes can lock out legitimate administrators if allow rules are incomplete before UFW is enabled or public SSH access is removed. <br>
Mitigation: Add and test explicit SSH allow rules, especially for the intended Tailscale path, before enabling default-deny rules or deleting public SSH access. <br>
Risk: The Tailscale step uses a remote script execution pattern. <br>
Mitigation: Prefer Tailscale's signed package repository or inspect the installer before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kime541200/openclaw-server-secure-skill) <br>
- [Tailscale install script](https://tailscale.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes server-level security changes that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
