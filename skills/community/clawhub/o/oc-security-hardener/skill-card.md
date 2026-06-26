## Description: <br>
Audits and hardens OpenClaw configuration by scanning openclaw.json for vulnerabilities, exposed credentials, insecure gateway settings, overly permissive exec rules, and missing security best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw deployments, review security findings, apply selected hardening fixes, scan for exposed credentials, and generate security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-fix commands can persistently change gateway binding, authentication options, exec sandboxing, and file permissions. <br>
Mitigation: Start with read-only audit or report commands, review the findings and generated backup, and run fixes only for changes you intend to apply. <br>
Risk: Reports and backup files can reveal security posture and may include original configuration contents. <br>
Mitigation: Treat generated reports and backups as sensitive files, restrict access to them, and avoid sharing them publicly. <br>
Risk: Secret scanning may identify credentials in local configuration output. <br>
Mitigation: Review results locally, move exposed secrets into environment-managed storage, and redact findings before sharing output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/oc-security-hardener) <br>
- [Publisher profile](https://clawhub.ai/user/mariusfit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, and Markdown reports with command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local backup files before applying fixes and may write Markdown security reports when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
