## Description:

Set up, repair, or document a Proxima deployment on a remote Ubuntu VPS with a non-root Electron runtime, virtual desktop GUI, loopback-only VNC/noVNC/REST exposure, and SSH-stdio MCP access for local IDEs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alkindivv](https://clawhub.ai/user/alkindivv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, repair, validate, or document Proxima on an Ubuntu VPS with remote GUI, REST, and MCP access kept behind loopback bindings and SSH transport.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags over-privileged and mutable deployment choices before installation.

Mitigation: Pin the Proxima source to a reviewed commit or release, use locked dependency installation, and review the setup before running it.

Risk: REST, VNC, noVNC, and MCP control surfaces can create exposure risk if made public.

Mitigation: Keep REST, VNC, noVNC, and MCP loopback-only, access them through SSH tunnels or SSH stdio, and use a dedicated non-root SSH identity.

Risk: Running browser automation with provider sessions and file access on a primary machine carries operational risk.

Mitigation: Install on an isolated VPS or VM and run the application under a restricted non-root account.

## Reference(s):

- [Proxima VPS Setup Skill](https://clawhub.ai/alkindivv/skills/proxima-vps)
- [Security and architecture](references/security-and-architecture.md)
- [Server setup runbook](references/server-setup-runbook.md)
- [Local access and MCP](references/local-access-and-mcp.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash, sshconfig, JSON, and systemd configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status reports include service health, loopback listener checks, REST validation, SSH-stdio MCP validation, and remaining blockers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
