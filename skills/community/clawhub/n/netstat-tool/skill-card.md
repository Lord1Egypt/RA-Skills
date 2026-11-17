## Description:

Display network connections, routing tables, and interface statistics for network diagnostics and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to inspect local network sockets, listening ports, routing information, and interface statistics during troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose local listening ports and network socket information.

Mitigation: Install and run it only in environments where local network diagnostics are appropriate and review output before sharing it.

Risk: The documented options describe broader netstat behavior than the bundled script currently implements.

Mitigation: Validate expected command behavior before relying on the skill for complete routing table, interface, process, TCP-only, UDP-only, or numeric-address diagnostics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/netstat-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local network diagnostic output may include listening ports, socket addresses, and service metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
