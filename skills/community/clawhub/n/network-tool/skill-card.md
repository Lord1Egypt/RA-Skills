## Description: <br>
Display and manage network interfaces, connections, and routing information. Use for network diagnostics and configuration analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill to inspect network interfaces, active connections, routes, DNS resolution, public IP information, and basic connectivity behavior during diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound HTTP requests and active network probes can contact systems outside the user's environment. <br>
Mitigation: Run curl, ping, DNS, speed-test, and public-IP checks only where outbound network testing is authorized. <br>
Risk: Port checks and port-range scans can be inappropriate or disruptive when used against systems the user does not own or administer. <br>
Mitigation: Limit port checks and scans to owned or explicitly authorized hosts and ranges. <br>
Risk: The skill description under-discloses broader active probing and arbitrary HTTP request behavior. <br>
Mitigation: Review the available commands before installation and document approved use boundaries for the target environment. <br>


## Reference(s): <br>
- [Network Tool on ClawHub](https://clawhub.ai/dinghaibin/network-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display network interface, routing, DNS, HTTP response, port, public IP, and speed-test information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
