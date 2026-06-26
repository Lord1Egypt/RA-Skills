## Description: <br>
OpenClaw Security Auditor audits OpenClaw deployments by scanning configuration, scoring risk, producing bilingual reports, and suggesting remediation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Albertlsy588](https://clawhub.ai/user/Albertlsy588) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw security configuration, classify findings by severity, generate reports, and receive remediation guidance before deployment or during hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner imports an external OSA dependency from outside the skill package. <br>
Mitigation: Review and verify the external dependency and its code path before running the scanner. <br>
Risk: The configuration fixer can weaken OpenClaw security settings, especially when aggressive mode is used. <br>
Mitigation: Use dry-run first, keep backups, prefer conservative or balanced modes, and reserve aggressive mode for isolated test environments. <br>
Risk: Generated reports can expose sensitive configuration details or tokens if shared directly. <br>
Mitigation: Mask tokens and sensitive paths before sharing reports outside the trusted environment. <br>


## Reference(s): <br>
- [OpenClaw Security Configuration Guide](references/config-guide.md) <br>
- [OpenClaw Security Modes](references/security-modes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Albertlsy588/openclaw-security-auditor-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, HTML, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown, JSON, HTML, or bilingual security audit report with risk scores and remediation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include configuration paths, findings, risk scores, and recommended fixes; mask tokens before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
