## Description:

Scans specified network targets and ports using nmap with options for speed, timeout, host limits, and exclusions, returning detailed JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apacheua](https://clawhub.ai/user/apacheua)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to run authorized nmap scans against specified IP addresses, IP ranges, or CIDR targets and receive structured scan results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can probe broad networks or run aggressive scans.

Mitigation: Use only for authorized targets in a controlled environment, and avoid broad CIDR or aggressive scans unless explicitly approved.

Risk: Weak input validation can allow requests to change nmap behavior beyond the documented options.

Mitigation: Restrict use to trusted users or agents, and add strict validation for targets, ports, and scan options before exposing it to untrusted input.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apacheua/skills/network-scan)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scan results, the nmap command used, and scan information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
