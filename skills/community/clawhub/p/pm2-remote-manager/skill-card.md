## Description:

SSH-based PM2 service management for remote servers. List processes, restart/stop services, view logs, monitor CPU/memory usage, and perform common PM2 operations on production servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoohsuan](https://clawhub.ai/user/qoohsuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to prepare and review SSH commands for monitoring, restarting, stopping, scaling, and troubleshooting PM2-managed Node.js services on remote servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote PM2 commands can interrupt production services when run against the wrong server, process, or account.

Mitigation: Confirm the SSH target, process name or ID, account privileges, and command scope before running restart, stop, delete, kill, flush, or startup-persistence commands.

Risk: Log and status commands can expose operational details from remote services.

Mitigation: Review log output handling and avoid sharing command results outside the operational context where the server data is authorized.

Risk: Installing unpinned PM2 modules can change the remote host environment.

Mitigation: Review module source and version before installation, and prefer a controlled maintenance window for host-level PM2 changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing command guidance; execution requires valid SSH access and human confirmation of the target server, process, and privilege level.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
