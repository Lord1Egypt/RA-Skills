## Description: <br>
Security audit and credential hardening tool for OpenClaw instances. Scan for sensitive files, detect credential exposure, check gateway configuration, and migrate credentials to environment variables. Essential for maintaining a secure OpenClaw deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vincent-Big-fish](https://clawhub.ai/user/Vincent-Big-fish) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit local OpenClaw configuration for sensitive files, exposed credentials, gateway security issues, and to migrate credentials into environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hardening workflow reads and modifies local OpenClaw configuration that may contain real credentials. <br>
Mitigation: Review changes before running harden.py, keep generated .env files, backups, and setup scripts out of source control and synced folders, restrict file permissions, and rotate credentials if any generated files are exposed. <br>
Risk: Audit reports and generated files may still reveal sensitive configuration context even when credential values are masked. <br>
Mitigation: Store outputs locally, limit access to trusted users, and inspect reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Vincent-Big-fish/openclaw-safe-audit) <br>
- [Publisher Profile](https://clawhub.ai/user/Vincent-Big-fish) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts produce JSON audit reports and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against ~/.openclaw and may create reports, backups, .env files, and platform setup scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
