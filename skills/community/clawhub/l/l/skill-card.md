## Description:

Short alias skill for listing files, directories, processes, or system information. Use when you need to see what's present in a directory or system state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill as a compact command reference for listing files, directories, processes, network connections, environment state, routes, firewall rules, and related system information across Linux, macOS, Windows, and PowerShell.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad listing requests can disclose sensitive local system details such as environment variables, process lists, routes, firewall rules, or network listeners.

Mitigation: Use explicit, narrow requests and redact tokens, passwords, keys, cookies, usernames, hostnames, and internal service details before sharing outputs.

Risk: Cross-platform command variants may reveal more information than intended when copied without review.

Mitigation: Review commands before running them and prefer scoped paths, process filters, ports, or fields that match the immediate task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/l)
- [ClawHub publisher profile](https://clawhub.ai/user/openlang-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
