## Description:

Configure firewalls on servers and cloud providers with security best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonzachee](https://clawhub.ai/user/gonzachee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as firewall guidance for servers and cloud providers, including SSH access safety, default deny rules, provider firewalls, IP restrictions, Docker exposure, IPv6, and debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firewall changes can lock out remote access if SSH or the management path is blocked.

Mitigation: Confirm required ports and IP ranges, keep provider console or another recovery path available, and test remote access in a second session before closing the first.

Risk: Opening unnecessary ports or exposing databases can increase attack surface.

Mitigation: Open only explicitly needed services, prefer private networks or SSH tunnels for databases, and review temporary rules for removal.

Risk: Docker and IPv6 behavior can bypass or differ from expected host firewall coverage.

Mitigation: Check Docker port bindings and provider-level controls, and configure both IPv4 and IPv6 rules where applicable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gonzachee/skills/my-firewall-v2)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with possible inline shell commands or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, credential handling, persistence, or hidden behavior identified in security evidence.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
