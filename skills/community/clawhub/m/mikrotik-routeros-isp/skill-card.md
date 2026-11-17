## Description:

Provides expert guidance and examples for managing MikroTik RouterOS devices and VSOL GPON OLTs through SSH, RouterOS API, and REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charllesvale](https://clawhub.ai/user/charllesvale)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators, ISP engineers, and agent developers use this skill to inspect and configure RouterOS and VSOL infrastructure, automate RouterOS API tasks, prepare backups, and draft failover or notification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential examples can expose router or OLT access if passwords are stored in shared files or command lines.

Mitigation: Prefer SSH keys or verified TLS, keep secrets out of TOOLS.md and command history, and use least-privilege device accounts.

Risk: Plaintext RouterOS API or unverified REST connections can expose management traffic.

Mitigation: Avoid API port 8728 for sensitive environments; use RouterOS API over TLS or REST with verified certificates where available.

Risk: Router configuration changes can interrupt live ISP services or lock out management access.

Mitigation: Read current state first, export or back up configuration before major changes, and require explicit review before destructive or broad-privilege commands.

Risk: Automatic third-party RouterOS script updates can introduce unreviewed changes on production devices.

Mitigation: Pin, audit, and internally host third-party scripts, and disable unattended updates on production routers.

## Reference(s):

- [RouterOS Command Reference](references/routeros-commands.md)
- [RouterOS API + REST API Reference](references/routeros-api.md)
- [Failover Actions + Notifications](references/failover-notifications.md)
- [eworm-de/routeros-scripts Reference](references/eworm-scripts.md)
- [VSOL GPON OLT SSH Reference](references/vsol-olt.md)
- [ISP Stack Reference](references/isp-stack.md)
- [MikroTik RouterOS Documentation](https://help.mikrotik.com/docs)
- [eworm RouterOS Scripts Documentation](https://rsc.eworm.de/main/)
- [eworm-de/routeros-scripts](https://github.com/eworm-de/routeros-scripts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with RouterOS, shell, Python, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device commands that should be reviewed before execution on production routers.]

## Skill Version(s):

2.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
