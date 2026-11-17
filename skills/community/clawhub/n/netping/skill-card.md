## Description:

Netping checks network connectivity with ping, port checks, DNS lookups, traceroute, latency measurement, HTTP checks, and subnet sweep commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and operators use Netping to troubleshoot reachability, DNS resolution, latency, HTTP response timing, traceroutes, TCP ports, and /24 subnet availability on authorized networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Port checks, traceroute, HTTP probes, and subnet sweeps are active network testing and may trigger monitoring or violate policy on unauthorized systems.

Mitigation: Run these commands only against hosts and networks you own or are authorized to assess, and review targets before executing scan-oriented commands.

## Reference(s):

- [Netping ClawHub page](https://clawhub.ai/ckchzh/skills/netping)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text diagnostic results and concise shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs active network diagnostics against user-specified hosts, ports, URLs, domains, or subnets.]

## Skill Version(s):

3.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
