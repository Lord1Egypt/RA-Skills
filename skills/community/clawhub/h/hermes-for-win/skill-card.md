## Description:

Installs, deploys, and manages hermes Agent and hermes-webui on Windows with WSL2, auto-start, background operation, updates, and status commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows users use this skill to install, configure, start, stop, update, and inspect a local hermes Agent and hermes-webui deployment through PowerShell and WSL2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to install Windows and WSL services using scripts that were not present for scanner inspection.

Mitigation: Install only after inspecting the PowerShell scripts from a trusted source and confirming the repositories and release artifacts they download.

Risk: Automatic updates and persistent startup can change or run local services without repeated manual review.

Mitigation: Review update targets before applying updates and enable auto-start only when persistent local execution is required.

Risk: The documented scheduled task may run with highest privileges and WSL files may contain sensitive configuration.

Mitigation: Use the least privilege that works, protect the Windows account and WSL files, and remove the scheduled task and WSL installation data during uninstall.

## Reference(s):

- [Hermes For Win ClawHub page](https://clawhub.ai/edwardwason/skills/hermes-for-win)
- [Reference Documentation](references/README.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command blocks and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows 10/11, WSL2, Ubuntu, and local PowerShell execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
