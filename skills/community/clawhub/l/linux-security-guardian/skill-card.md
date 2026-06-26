## Description: <br>
Autonomous Linux server security management skill for multi-client SSH audits, CVE scanning, controlled hardening actions, and security reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
System administrators and security engineers use this skill to run recurring Linux server audits across client server fleets, review findings, and manage confirm-gated remediation. It is intended for environments where the operator is prepared to grant administrative SSH access and review sensitive security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run recurring administrative SSH audits and approved actions across multiple servers. <br>
Mitigation: Install only where that access is intended, restrict the auto-action whitelist, remove or constrain broad approval language, and keep confirmation required for critical, patching, and firewall changes. <br>
Risk: Security findings, reports, caches, and emails may contain sensitive server and vulnerability details. <br>
Mitigation: Protect report and cache directories, verify per-client email recipients before enabling reports, and limit access to generated findings. <br>
Risk: External CVE lookups may disclose package and version data to vulnerability data providers. <br>
Mitigation: Decide before deployment whether CISA, OSV.dev, and NVD lookups are permitted for the environment, and disable or constrain external sources where policy requires it. <br>
Risk: Automated remediation can cause outages if actions are too broad or rollback handling is incomplete. <br>
Mitigation: Review rollback-script handling, test changes on non-critical systems, and require explicit approval for disruptive service, package, kernel, and network changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyber-bye/linux-security-guardian) <br>
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) <br>
- [CISA KEV JSON feed](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) <br>
- [OSV.dev API documentation](https://google.github.io/osv.dev/) <br>
- [NVD API documentation](https://nvd.nist.gov/developers/start-here) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, pending-action records, configuration notes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized by client and server and may include audit findings, CVE advisories, proposed changes, rollback notes, and email-ready reports.] <br>

## Skill Version(s): <br>
1.4.2 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
