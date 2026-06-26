## Description: <br>
Helps agents set up Hostinger VPS servers as AI assistant workstations with GUI access, Docker, OpenClaw/Koda deployment, Hostinger API MCP integration, and post-deployment hardening guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to provision and configure Hostinger VPS instances as remotely accessible AI workstations. It supports Hostinger API MCP setup, server bootstrapping, GUI installation, Docker and OpenClaw/Koda deployment, and identity configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Hostinger API token and run root-level provisioning scripts, giving it broad infrastructure authority. <br>
Mitigation: Review the scripts before execution, run them on a fresh VPS, use the least-privileged rotatable Hostinger token available, and rotate any token that may have been displayed or entered in shell commands. <br>
Risk: Default deployment paths can expose SSH, RDP, and webchat services on public network ports. <br>
Mitigation: Verify SSH host keys yourself, prefer VPN or tunnel access, and use the included public-access lockdown or equivalent firewall controls before relying on the server. <br>
Risk: Automation may create broad local privileges such as passwordless sudo for the deployed user. <br>
Mitigation: Remove or narrow passwordless sudo after setup and confirm account, firewall, and remote access settings match the intended operating model. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/maverick-software/hostinger-vps-mcp-tools) <br>
- [Hostinger API Reference](https://developers.hostinger.com/) <br>
- [Hostinger API Authentication](https://developers.hostinger.com/#description/authentication) <br>
- [Hostinger Official MCP Server](https://github.com/hostinger/api-mcp-server) <br>
- [hPanel API Tokens](https://hpanel.hostinger.com/api-tokens) <br>
- [hostinger-backend.ts](references/hostinger-backend.ts) <br>
- [hostinger-controller.ts](references/hostinger-controller.ts) <br>
- [hostinger-views.ts](references/hostinger-views.ts) <br>
- [Hostinger VPS Notes](references/hostinger-notes.md) <br>
- [Virtual Employee Identity Setup](references/identity-setup.md) <br>
- [Security Options](references/security-options.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and reference code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include root-level VPS provisioning steps, Hostinger API MCP calls, and post-deployment hardening guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
