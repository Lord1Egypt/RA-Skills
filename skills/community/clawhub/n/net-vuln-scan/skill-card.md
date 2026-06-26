## Description: <br>
net-vuln-scan helps agents assess authorized hosts and network services for exposed ports, weak or default credentials, SSL/TLS issues, service vulnerabilities, risky network configuration, and sensitive information exposure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aritz-China](https://clawhub.ai/user/Aritz-China) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, system administrators, and developers use this skill to run authorized security self-checks on local, internal, or administered hosts before audits, penetration-test preparation, hardening work, or server release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide port scans, weak-password checks, cloud metadata probes, and remediation commands that may be inappropriate or unauthorized on systems outside the user's control. <br>
Mitigation: Use it only for systems the user owns or administers, restrict target scope before running commands, and require explicit authorization for scanning or remediation. <br>
Risk: The security evidence warns that vulnerability claims are overstated and CVE results are rough indicators. <br>
Mitigation: Verify findings with vendor advisories or established scanners before treating them as confirmed vulnerabilities or making operational changes. <br>
Risk: Artifact examples include commands that can alter firewall, authentication, package, service, or cloud metadata settings. <br>
Mitigation: Review generated commands before execution, test changes in an appropriate environment, and apply least-privilege administrative controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Aritz-China/net-vuln-scan) <br>
- [Usage examples](references/examples.md) <br>
- [Port scan guide](references/port_scan_guide.md) <br>
- [SSL check guide](references/ssl_check_guide.md) <br>
- [Weak password guide](references/weakpass_guide.md) <br>
- [Latest vulnerabilities 2026](references/latest_vulnerabilities_2026.md) <br>
- [Platform vulnerabilities 2026](references/platform_vulnerabilities_2026.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-style security reports with inline shell commands and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include risk-ranked findings, affected services or ports, descriptions, recommendations, and reference links.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
