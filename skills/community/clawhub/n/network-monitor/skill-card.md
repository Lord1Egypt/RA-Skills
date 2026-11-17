## Description:

Network Monitor helps inspect local network interfaces, active connections, listening ports, bandwidth, latency, DNS, whois, traceroute, and download speed from shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for local network diagnostics, connectivity checks, and concise command output for troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The DNS command has an input handling bug that can execute arbitrary Python code as the user running the skill.

Mitigation: Review and fix DNS argument handling before use; avoid running the DNS command with untrusted domains until remediated.

Risk: The skill inspects local network metadata and performs outbound diagnostics, including a speed test to a third-party HTTP host.

Mitigation: Run only in environments where local network inspection and outbound diagnostic traffic are approved, and disclose this behavior to users before deployment.

## Reference(s):

- [Network Monitor on ClawHub](https://clawhub.ai/bytesagain-lab/skills/network-monitor)
- [GyulyVGC/sniffnet reference project](https://github.com/GyulyVGC/sniffnet)
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with concise diagnostic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local network metadata and may initiate outbound diagnostic requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
