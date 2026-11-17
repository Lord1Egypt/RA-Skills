## Description:

Dragon-class High Availability (HA) guardian with metabolic cleansing and 3-tier self-healing for OpenClaw environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxleolee-eng](https://clawhub.ai/user/maxleolee-eng)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to maintain an OpenClaw environment with heartbeat monitoring, scheduled maintenance, backups, and staged recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent recovery service can restart OpenClaw, kill processes, and alter local sessions and configuration.

Mitigation: Install only on systems where that authority is intended, review the LaunchAgent or service setup before enabling it, and keep an explicit stop or uninstall path available.

Risk: Recovery and restore scripts can rewrite configuration, restore credential-bearing files, delete caches or logs, and reinstall global packages.

Mitigation: Require manual confirmation before running destructive scripts, verify current backups, pin package versions where practical, and avoid unattended use of reinstall paths.

Risk: Backup vaults and restored workspace files may contain sensitive configuration, auth profiles, or agent instructions.

Mitigation: Protect backup locations with restrictive permissions or encryption and review restored AGENTS.md, MEMORY.md, and configuration files as untrusted content before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxleolee-eng/skills/openclaw-sys-guardian-v4-1-resurrection)
- [Architecture](references/Architecture.md)
- [Design](references/Design.md)
- [Design V4.5](references/Design_V4.5.md)
- [Full Manual](references/FullManual.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and bundled shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for macOS or Linux OpenClaw environments.]

## Skill Version(s):

4.1.7 (source: server release evidence; skill frontmatter lists 4.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
