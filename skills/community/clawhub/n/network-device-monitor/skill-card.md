## Description:

Monitor network devices, detect unknown clients, and alert on new connections. Works with any router that serves a web UI. Tracks device state changes over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT operators, and network administrators use this skill to scan authorized local networks, compare detected devices against a known-device list, and surface new or unknown clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network scanning can be inappropriate or unauthorized on shared, corporate, or sensitive networks.

Mitigation: Run scans only on networks where the operator has authorization, and use a narrow validated subnet.

Risk: ARP mode scans the local network segment and may go beyond the requested subnet.

Mitigation: Prefer non-root nmap mode; use ARP mode only when segment-wide scanning is understood and authorized.

Risk: Discovered device identifiers are stored locally in a state file.

Mitigation: Treat the state file as sensitive local data, choose an explicit protected path when needed, and remove it when no longer required.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; scan output can be plain text, table text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State is stored locally in a JSON file unless a different state path is supplied.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
