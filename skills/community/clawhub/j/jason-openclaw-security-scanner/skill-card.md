## Description: <br>
Scans OpenClaw configuration, permissions, files, sensitive data, and logs to produce a security score, findings, and repair recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ITHACAJASON](https://clawhub.ai/user/ITHACAJASON) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run local OpenClaw security checks, understand findings, and choose interactive or targeted fixes for configuration, permission, secret-handling, and audit issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair modes can change local files such as TOOLS.md, AGENTS.md, .gitignore, or file permissions. <br>
Mitigation: Run the default scan first, prefer interactive or targeted fixes, and review proposed changes before applying them. <br>
Risk: Security reports may reference sensitive configuration values or local paths. <br>
Mitigation: Keep console and JSON reports private and avoid sharing them without redaction. <br>
Risk: Adding a secret-bearing file to .gitignore does not remediate credentials that were already exposed. <br>
Mitigation: Rotate and remove exposed credentials separately when the scanner reports them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ITHACAJASON/jason-openclaw-security-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style security report with inline shell commands and repair guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include security scores, findings, and repair recommendations; repair modes can modify local configuration files, ignore rules, or file permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
