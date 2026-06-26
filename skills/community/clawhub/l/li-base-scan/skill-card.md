## Description: <br>
Li Base Scan helps agents run authorized single-host Linux security baseline scans with nmap, lynis, nikto, sqlmap, and trivy, then produce scan findings and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, system administrators, and developers use this skill to run authorized single-host baseline, web, compliance, and vulnerability scans and export findings for remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized or stealth scanning can create legal, operational, or monitoring-impact risk. <br>
Mitigation: Scan only systems you own or are explicitly authorized to test, and avoid stealth mode unless it is approved for the engagement. <br>
Risk: Full and compliance modes may scan the local agent filesystem for vulnerabilities, misconfigurations, and secrets. <br>
Mitigation: Run the skill in an isolated, low-privilege environment and use narrower scan modes unless local filesystem scanning is intended. <br>
Risk: Saved reports and scan history may contain sensitive security findings or target-derived metadata. <br>
Mitigation: Protect report and history files with restrictive permissions, review retention needs, and delete exported artifacts when no longer needed. <br>
Risk: The documented dependency installation path includes a curl-to-shell command. <br>
Mitigation: Use verified packages or pinned installer versions instead of executing an unpinned remote install script. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/43622283/li-base-scan) <br>
- [Publisher profile](https://clawhub.ai/user/43622283) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, guidance] <br>
**Output Format:** [Console text, JSON, Markdown, or HTML reports containing scan findings and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save scan reports and SQLite history on the local filesystem.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
