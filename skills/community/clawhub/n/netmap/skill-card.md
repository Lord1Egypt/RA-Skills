## Description: <br>
Scans and maps devices on the local network, including IP addresses, hostnames, vendors, device types, first and last seen times, friendly labels, and search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrentheai](https://clawhub.ai/user/wrentheai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and users responsible for home or office networks use Netmap to inventory local devices, find device IPs, identify new or unknown devices, and troubleshoot local connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local network inventory, including IP addresses, MAC addresses, hostnames, labels, vendors, and first or last seen times, may be stored on disk. <br>
Mitigation: Use the skill only on networks you own or administer, protect the local device database, and remove exported or stored inventory when it is no longer needed. <br>
Risk: MAC addresses may be sent to api.macvendors.com for vendor lookup. <br>
Mitigation: Avoid the online vendor lookup in privacy-sensitive environments, or disable/remove that behavior before use. <br>
Risk: Running scans with sudo or deep port scanning can increase privacy and operational impact on a local network. <br>
Mitigation: Avoid sudo unless MAC address visibility is required, prefer fast scans for routine refreshes, and get authorization before scanning shared or managed networks. <br>


## Reference(s): <br>
- [Netmap on ClawHub](https://clawhub.ai/wrentheai/netmap) <br>
- [MacVendors API](https://api.macvendors.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce and update a local JSON device database under the user's home configuration directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
