## Description:

Analyze IP addresses with subnet calculation and CIDR notation. Use when planning network addressing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network operators use this skill to inspect IPv4 addresses, check simple private/public classification, view CIDR mask bits, validate address format, and retrieve local or public interface information during network planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public-IP command contacts Amazon's checkip service, which discloses the machine's outbound public IP address to that service.

Mitigation: Use the public command only when external public-IP disclosure is acceptable for the current network environment.

Risk: The local command can reveal local network interface addresses and related interface details.

Mitigation: Avoid running the local command in sensitive environments unless exposing local interface details is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/ip-advisor)
- [Publisher Profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain Homepage](https://bytesagain.com)
- [Amazon Check IP Service](https://checkip.amazonaws.com)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local data directory at ~/.local/share/ip-advisor and may call an external public-IP endpoint when the public command is used.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
