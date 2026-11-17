## Description:

Tells an agent what changed on a server since it last looked - plus status, Docker, backups, Proxmox. Every tool is classed read, write or destructive, so an agent can tell a look from a change before it makes the call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[higangssh](https://clawhub.ai/user/higangssh)

### License/Terms of Use:

MIT-0

## Use Case:

Server operators and developers use Homebutler through an agent to review infrastructure changes and inspect Docker, backups, and Proxmox. They can also request server operations, with write and destructive actions identified for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented operations include software installation, deployment, upgrades, and removal, which can change a server or its services.

Mitigation: Review each high-impact action and its target before allowing it; require a specific request for destructive operations.

Risk: The security assessment has medium confidence because the scan was partial and several referenced paths were missing.

Mitigation: Review the complete release files and the target-specific action before installation or server changes.

Risk: Remote reads can return hostnames, internal addresses, usernames, and log contents.

Mitigation: Share only the relevant findings and avoid forwarding raw logs or full inventory output.

## Reference(s):

- [Homebutler on ClawHub](https://clawhub.ai/higangssh/skills/homebutler)

## Skill Output:

**Output Type(s):** [Guidance, MCP tool calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with MCP tool names, shell examples, and structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and results depend on the requested operation and configured servers.]

## Skill Version(s):

2.8.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
