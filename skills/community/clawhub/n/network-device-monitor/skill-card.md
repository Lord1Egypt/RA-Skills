## Description: <br>
Monitors network devices across a subnet, detects unknown clients, and tracks device state changes over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT operators, and home-lab administrators use this skill to run authorized local network scans, compare detected devices with a known-device list, and surface unknown or changed devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs local network discovery and can expose device inventory information. <br>
Mitigation: Use it only on networks you are authorized to scan, keep scan ranges narrow, and protect or delete saved state files that contain sensitive inventory. <br>
Risk: ARP scan mode may require elevated privileges on the local machine. <br>
Mitigation: Prefer non-root nmap mode when possible and grant elevated privileges only for authorized scans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hostilespider/network-device-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output can be plain text, table text, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local state JSON file for device history and optional known-device JSON configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
