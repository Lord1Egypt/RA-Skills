## Description:

Linux base security scanner integrating multiple tools - nmap, lynis, nikto, sqlmap, trivy. SINGLE HOST ONLY. Features secure temp files, progress bar, scan history, report export. Comprehensive security baseline scanning with hardened implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and authorized operators use this skill to run single-host Linux baseline, network, web, SQL injection, container or filesystem vulnerability, and compliance scans, then review generated findings and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise broad local and network scanning authority.

Mitigation: Run it as an unprivileged user and scan only systems you own or have explicit authorization to test.

Risk: Stealth scans and sqlmap checks can be intrusive, evasive, or disruptive in production environments.

Mitigation: Avoid stealth mode and sqlmap against production targets unless written approval and a defined test window are in place.

Risk: Filesystem vulnerability and secret scans can inspect sensitive local paths and produce sensitive reports.

Mitigation: Limit scan scope where possible, protect generated reports and history files, and review report contents before sharing.

Risk: The artifact documentation includes a curl-piped Trivy installer command.

Mitigation: Install dependencies through trusted package manager or verified vendor channels instead of using the curl | sh line.

Risk: Caller-supplied HTML report paths may write reports outside intended locations.

Mitigation: Use controlled default output paths and avoid caller-supplied HTML report paths until path constraints and escaping are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-base-scan)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance]

**Output Format:** [Console text, JSON objects, Markdown reports, HTML reports, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include scan history entries and report files generated from local and network security tools.]

## Skill Version(s):

0.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
