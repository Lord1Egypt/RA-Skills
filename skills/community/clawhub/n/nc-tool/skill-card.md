## Description:

Read and write data across network connections using TCP or UDP. Use for network debugging, port scanning, and data transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network engineers use this skill for netcat-style network diagnostics, port checks, and basic connectivity testing on authorized hosts and networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network diagnostic, scan, or listen-style commands can affect systems outside the intended authorization boundary.

Mitigation: Use only on hosts and networks you own or are explicitly authorized to test, and confirm the target host and port range before execution.

Risk: The skill text describes broad netcat capabilities, while the bundled script evidence shows only a simple TCP connection check.

Mitigation: Verify the available behavior before relying on UDP, listen mode, data transfer, or full port-scanning workflows.

Risk: Network commands may send or receive data during testing.

Mitigation: Confirm whether data transfer is expected before running commands, and avoid sending sensitive data through test connections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/nc-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands and short explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
