## Description:

Net Vuln Scan helps an agent run authorized network and host security checks for open ports, weak or default credentials, SSL/TLS certificate issues, service vulnerabilities, network configuration risks, sensitive port exposure, and platform CVE checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aritz-china](https://clawhub.ai/user/aritz-china)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and security engineers use this skill to inspect systems they are authorized to test, summarize likely network and service risks, and generate remediation guidance before deployment or hardening work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for security scanning and could be misused against systems without authorization.

Mitigation: Use only on systems where testing is explicitly authorized, and review each proposed scan command before running it.

Risk: The release security evidence flags under-scoped cloud metadata probing.

Mitigation: Do not run the all-platform scan on cloud-hosted systems unless cloud metadata probing is explicitly in scope.

Risk: The release security evidence flags a report-generation issue that can affect generated HTML reports from untrusted input.

Mitigation: Treat generated HTML reports as unsafe when the source JSON was supplied by another party, and open reports only in a controlled environment.

Risk: Remediation examples include firewall, SSH, sudo, and package-management commands that can change production systems.

Mitigation: Review commands against the target operating environment and change-control process before applying them.

## Reference(s):

- [Skill page](https://clawhub.ai/aritz-china/skills/net-vuln-scan)
- [Examples](references/examples.md)
- [Port Scan Guide](references/port_scan_guide.md)
- [SSL/TLS Certificate Check Guide](references/ssl_check_guide.md)
- [Weak Password Check Guide](references/weakpass_guide.md)
- [2026 Vulnerabilities and Remediation Guide](references/latest_vulnerabilities_2026.md)
- [Platform Vulnerabilities Summary](references/platform_vulnerabilities_2026.md)
- [Microsoft Security Update Guide: CVE-2026-21514](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-21514)
- [Microsoft Security Update Guide: CVE-2026-21262](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-21262)
- [.NET Download](https://dotnet.microsoft.com/download/dotnet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell and Python commands; bundled scripts can generate terminal output plus JSON and HTML security reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked vulnerability findings, descriptions, impact notes, remediation steps, and reference links.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
