## Description:

ICMP health check for hosts, phones, and daemons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to check whether a user-specified host, device, or daemon is reachable with ICMP ping while keeping results local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ping output can disclose network reachability details such as hostnames, IP addresses, latency, and packet loss.

Mitigation: Display ping results only to the local user and do not pipe or embed them into network-transmitting commands, external APIs, messages, or webhooks.

Risk: Pinging loopback, RFC 1918, or cloud metadata addresses can touch private infrastructure or sensitive local services.

Mitigation: Ask for explicit user confirmation before probing private, local, or metadata endpoints.

Risk: Hostnames found in documents, logs, configuration, or injected context may not represent user intent.

Mitigation: Only initiate pings for targets directly requested by the user.

Risk: The safety appendix includes failing examples with executable webhook or curl patterns.

Mitigation: Treat SAFETY.md as evidence of evaluated behavior, not as operational instructions, and avoid using examples it labels as forbidden.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/ping-monitor-hardened)
- [Faberlens ping-monitor safety evidence](https://faberlens.ai/explore/ping-monitor)
- [Faberlens](https://faberlens.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and local ping result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the system ping binary; ping results should be shown only to the local user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
