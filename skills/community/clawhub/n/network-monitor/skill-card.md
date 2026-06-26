## Description: <br>
Network Monitor helps agents inspect local network interfaces, active connections, listening ports, bandwidth, latency, routes, DNS, whois data, and download speed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to request local network diagnostics from an agent, including interface status, connection summaries, port listeners, bandwidth estimates, latency checks, DNS lookups, whois results, traceroute output, and a simple download speed test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS lookups can run unintended local code if the domain argument contains crafted text. <br>
Mitigation: Do not pass untrusted domain strings to the DNS command until the publisher fixes the command construction. <br>
Risk: Network diagnostics can expose local network interfaces, connection details, ports, routes, DNS results, whois output, and other environment-specific data. <br>
Mitigation: Install and run the skill only when local network diagnostics are needed, and review command output before sharing it. <br>
Risk: The speed test contacts an external HTTP endpoint. <br>
Mitigation: Run the speed command only in environments where outbound contact to the speed-test service is acceptable. <br>


## Reference(s): <br>
- [Network Monitor on ClawHub](https://clawhub.ai/bytesagain-lab/network-monitor) <br>
- [Publisher profile: bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>
- [GyulyVGC/sniffnet reference project](https://github.com/GyulyVGC/sniffnet) <br>
- [Tele2 speed test endpoint](http://speedtest.tele2.net/1MB.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local network interface names, addresses, connection details, port listeners, DNS results, whois excerpts, latency measurements, traceroute paths, and speed-test results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
