## Description:

Linux Ops is a Chinese Linux operations quick reference for process management, log analysis, network diagnostics, performance monitoring, and user management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afine907](https://clawhub.ai/user/afine907)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and operations engineers use this skill as a concise Linux command reference for routine host inspection, troubleshooting, and administrative tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative command examples can change accounts, permissions, firewall state, services, packet captures, or sudo behavior on real systems.

Mitigation: Review commands before use, confirm the target host and resources, obtain explicit authorization, and apply least-privilege constraints.

Risk: Examples such as passwordless sudo, recursive chmod/chown, user deletion, service stop/enable, and firewall changes may cause outages or weaken security if copied directly.

Mitigation: Validate commands in a controlled environment first and prepare backups or rollback steps before running them on production systems.

## Reference(s):

- [Process Management](references/process.md)
- [System Resources](references/system.md)
- [Network Diagnostics](references/network.md)
- [Log Analysis](references/logs.md)
- [User Permissions](references/users.md)
- [Linux Command Line Cheat Sheet](https://cheatography.com/davechild/cheat-sheets/linux-command-line/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language Linux operations quick reference.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
