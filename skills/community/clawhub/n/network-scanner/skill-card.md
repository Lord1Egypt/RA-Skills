## Description: <br>
Scan networks to discover devices, gather MAC addresses, vendors, and hostnames. Includes safety checks to prevent accidental scanning of public networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florianbeer](https://clawhub.ai/user/florianbeer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, network operators, and security auditors use this skill to inventory authorized private networks, identify devices, and produce network documentation from nmap and DNS results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Malformed CIDR, DNS, or config inputs could run unintended local commands because scan parameters are used to build shell commands. <br>
Mitigation: Review before installing, use only trusted network names, CIDRs, DNS values, and config files, and prefer --no-sudo unless MAC discovery is required. <br>
Risk: Network scans can affect systems outside the user's authorization if targets are chosen carelessly. <br>
Mitigation: Use only on networks you own or are authorized to scan, keep public-range blocking enabled, and maintain a blocklist for networks that should never be scanned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/florianbeer/network-scanner) <br>
- [Skill homepage](https://clawhub.com/skills/network-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown table by default, with optional JSON output and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires nmap and dig; sudo is optional for MAC address discovery.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
