## Description: <br>
Set up, repair, or document Proxima on a remote Ubuntu VPS with a non-root Electron runtime, loopback-only GUI and REST exposure, SSH-tunneled access, and SSH-stdio MCP configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alkindivv](https://clawhub.ai/user/alkindivv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install or repair Proxima on an isolated Ubuntu VPS, expose GUI and REST access through SSH tunnels, and configure local IDEs to reach Proxima MCP over SSH stdio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can normalize passwordless root SSH for routine tunnels and IDE MCP access on a high-authority VPS. <br>
Mitigation: Use root only for initial host setup where possible, prefer a dedicated non-root SSH account or narrowly scoped wrapper for ongoing access, and review SSH configuration before connecting IDEs. <br>
Risk: REST, VNC, noVNC, and MCP control surfaces can expose sensitive Proxima capabilities if bound publicly. <br>
Mitigation: Keep these services bound to localhost or authenticated SSH tunnels unless the user explicitly accepts a different exposure model. <br>
Risk: Running Proxima can carry operational risk from browser automation, provider sessions, file access, and dependencies. <br>
Mitigation: Run it on an isolated VPS or VM, review the Proxima repository and npm dependencies before installation, and avoid recommending it for a primary personal machine. <br>


## Reference(s): <br>
- [Security and architecture](references/security-and-architecture.md) <br>
- [Server setup runbook](references/server-setup-runbook.md) <br>
- [Local access and MCP](references/local-access-and-mcp.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, JSON, sshconfig, and systemd snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validation checks for service status, loopback listeners, REST health, SSH tunnels, and MCP stdio connectivity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
