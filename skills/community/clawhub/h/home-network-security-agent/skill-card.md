## Description:

Audits local network infrastructure, identifies active hosts, and scans the gateway/public IP for exposed ports and vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assix](https://clawhub.ai/user/assix)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and home network administrators use this skill to inventory local devices, identify gateway and public IP exposure, and review router or service scan results for security follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run active nmap scans against local or public targets without strong scope checks.

Mitigation: Use it only on networks and public IPs you own or are authorized to test, and add explicit target confirmation or an allowlist before deployment.

Risk: Deep scans can be intrusive and may take substantially longer than fast scans.

Mitigation: Avoid deep scans by default and require user confirmation before running full-port service detection.

Risk: The public-IP lookup discloses a request to an external service.

Mitigation: Disclose the lookup behavior to users and provide an opt-out or replacement endpoint when needed.

## Reference(s):

- [HomeNetworkSecurityAgent ClawHub page](https://clawhub.ai/assix/skills/home-network-security-agent)
- [ifconfig.me public IP endpoint](https://ifconfig.me/ip)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON scanner results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, nmap, and ip binaries; scan results depend on authorized network access and selected scan depth.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
