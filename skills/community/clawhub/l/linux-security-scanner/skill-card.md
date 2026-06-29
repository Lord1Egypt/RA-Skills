## Description: <br>
Linux Security Scanner helps audit a Linux host by checking SSH configuration, listening ports, firewall rules, failed logins, sudoers permissions, world-writable files, and SUID binaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laolaoqi](https://clawhub.ai/user/laolaoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security administrators use this skill to run local Linux security posture checks and collect a formatted audit report for hardening or compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output may expose sensitive host details, including usernames, IP addresses, open services, sudo privileges, firewall rules, and SUID paths. <br>
Mitigation: Run the scanner only on systems you own or administer, protect generated reports, and avoid sharing output publicly. <br>
Risk: Some checks require elevated privileges to inspect local security state. <br>
Mitigation: Use sudo only for checks that need it and review commands before running them on production systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laolaoqi/linux-security-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Colorized terminal output and structured Markdown audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some checks require root or sudo access; unsupported local tools are skipped gracefully.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
