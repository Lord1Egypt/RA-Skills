## Description: <br>
Enterprise-grade security framework for LobsterAI with audit logging, RBAC, input validation, output sanitization, code scanning, and dependency vulnerability detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoneyhoo](https://clawhub.ai/user/stoneyhoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add LobsterAI security utilities for audit logging, role-based authorization, input validation, output sanitization, code scanning, and dependency checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit integration script can permanently rewrite scripts in other installed skills. <br>
Mitigation: Run it only on backups or a test installation, review diffs before keeping changes, and avoid running it during normal installation unless that behavior is explicitly required. <br>
Risk: Audit logs may contain sensitive operational details and are less tamper-evident without an HMAC secret. <br>
Mitigation: Set LOBSTERAI_AUDIT_SECRET, restrict permissions on audit log directories, and review log retention and access policies before production use. <br>
Risk: Remote log forwarding can expose private activity or sensitive data if enabled without review. <br>
Mitigation: Do not enable remote forwarding until privacy, security, and destination access controls have been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stoneyhoo/lobsterai-security) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/stoneyhoo) <br>
- [Technical Documentation](artifact/TECHNICAL_DOCUMENTATION.md) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [Deployment Guide](artifact/DEPLOYMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, Python utilities, JSON log/configuration data, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create audit logs and, when the audit integration script is run, modify other skill scripts.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
