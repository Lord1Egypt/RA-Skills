## Description:

Scan networks to discover devices, gather MAC addresses, vendors, and hostnames. Includes safety checks to prevent accidental scanning of public networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbeer](https://clawhub.ai/user/florianbeer)

### License/Terms of Use:


## Use Case:

Developers, engineers, and network administrators use this skill to discover devices on authorized local or private networks, collect hostnames, MAC addresses, vendors, and produce network inventory or audit output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe command execution in the scanner.

Mitigation: Review or patch the script before use, and do not run it with untrusted network names, CIDRs, DNS values, or config files.

Risk: The security evidence reports weaker-than-advertised public-scan protections, especially around configured networks.

Mitigation: Limit configured networks to authorized private ranges, keep blocklists current, and prefer --no-sudo until public-target checks are strengthened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/florianbeer/skills/network-scanner)
- [Skill homepage](https://clawhub.com/skills/network-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown tables or JSON device inventories, with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires nmap and dig; sudo is recommended for MAC address discovery but --no-sudo is available.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
