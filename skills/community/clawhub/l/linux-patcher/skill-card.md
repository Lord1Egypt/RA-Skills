## Description:

Linux Patcher helps agents patch Linux servers and optionally update Docker containers over SSH, using PatchMon for automatic host detection when configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgm2025](https://clawhub.ai/user/jgm2025)

### License/Terms of Use:

MIT License

## Use Case:

Developers and infrastructure operators use this skill to check and apply Linux package updates, run dry-run maintenance workflows, and optionally update Docker Compose workloads across one or more SSH-accessible hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad production host access and passwordless sudo for patching and Docker commands.

Mitigation: Review the scripts before installation and grant sudo through narrow, audited wrappers or restricted command entries only.

Risk: PatchMon credentials, sourced configuration files, hostnames, users, and paths may affect remote commands.

Mitigation: Avoid sourcing generated or user-supplied configuration files without review, validate hostnames/users/paths, and keep credentials in a permissions-restricted file.

Risk: Some documented workflows use unsafe transport or install patterns such as curl -k and curl piped to sudo bash.

Mitigation: Remove curl -k usage, verify TLS certificates, and install PatchMon through reviewed packages or pinned, inspected scripts instead of piping downloads directly to sudo.

Risk: Docker image pulls and container recreation can change running services and cause downtime.

Mitigation: Keep Docker updates opt-in, use dry-run mode first, and schedule container updates during a maintenance window.

## Reference(s):

- [Linux Patcher ClawHub page](https://clawhub.ai/jgm2025/skills/linux-patcher)
- [PatchMon Integration Guide](references/patchmon-setup.md)
- [PatchMon GitHub repository](https://github.com/PatchMon/PatchMon)
- [PatchMon documentation](https://docs.patchmon.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide dry-run checks, package patching, PatchMon queries, and optional Docker Compose update workflows.]

## Skill Version(s):

3.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
