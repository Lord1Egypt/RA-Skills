## Description:

Display network connections, listening ports, and routing tables for network diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local network sockets, listening services, routes, DNS servers, and interface addresses while diagnosing network issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network diagnostic output can reveal local sockets, listening ports, routes, DNS servers, interfaces, and related process information.

Mitigation: Run the skill only in trusted local environments and review output before sharing it outside the diagnostic context.

Risk: The script creates a per-user data directory under ~/.local/share/netstat.

Mitigation: Install only when this local filesystem behavior is acceptable for the target user account.

## Reference(s):

- [Netstat skill page](https://clawhub.ai/bytesagain3/skills/netstat)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may display local socket, process, route, DNS, and interface information.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
