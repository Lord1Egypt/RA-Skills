## Description: <br>
OpenWRT router management and monitoring through the LuCI web interface, supporting DHCP lease lookup, online device listing, WiFi client management, network status checks, and related OpenWRT/LEDE router tasks without SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nary24](https://clawhub.ai/user/nary24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and technically capable router owners use this skill to let an agent inspect and manage OpenWRT routers through LuCI RPC. Typical tasks include reviewing connected devices, DHCP leases, WiFi clients, system status, installed packages, and package installation requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad remote shell control over a target OpenWRT router using administrator credentials. <br>
Mitigation: Install only for trusted agents, review commands before execution, and use the least-privileged router account available. <br>
Risk: Router credentials may be stored in shared project files or passed to commands. <br>
Mitigation: Avoid committing or sharing router passwords, restrict access to any configuration file that contains credentials, and rotate credentials if exposure is suspected. <br>
Risk: LuCI RPC requests may use plain HTTP on the local network. <br>
Mitigation: Prefer HTTPS or a trusted isolated network path, and avoid using the skill across untrusted networks. <br>
Risk: Package installation or shell commands can change router behavior or availability. <br>
Mitigation: Manually review package-install and configuration-changing requests before allowing the agent to run them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nary24/openwrt-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and router status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include LuCI RPC commands, parsed router inventory, DHCP lease summaries, WiFi client details, package lists, and operational guidance.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
