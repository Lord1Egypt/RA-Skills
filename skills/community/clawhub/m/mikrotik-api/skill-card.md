## Description: <br>
Manages MikroTik routers via the RouterOS API (port 8728/8729). Use when the user wants to configure, monitor, or troubleshoot a MikroTik router, including interfaces, firewall, DHCP, DNS, routing, queues, VPN, and system management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluemeda](https://clawhub.ai/user/bluemeda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and engineers use this skill to configure, monitor, troubleshoot, and automate MikroTik RouterOS devices through API or REST workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill administers a high-impact router management interface and can affect network availability or security. <br>
Mitigation: Use a limited RouterOS account, back up the router first, and review every command before deletes, firewall edits, updates, shutdowns, or reboots. <br>
Risk: The skill includes credential and TLS patterns that may be unsafe if copied directly. <br>
Mitigation: Avoid inline credentials and shared .env files, prefer verified TLS on a trusted management network, and do not disable certificate verification except for a reviewed exception. <br>
Risk: Installing dependencies directly into the system Python environment can affect other tools. <br>
Mitigation: Install dependencies in a virtual environment before using the RouterOS API library. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bluemeda/mikrotik-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, curl, and RouterOS command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include router administration steps that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
