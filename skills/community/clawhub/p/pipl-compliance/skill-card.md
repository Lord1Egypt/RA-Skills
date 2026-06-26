## Description: <br>
PIPL-Compliance（PIPL合规工具） helps teams run Chinese Personal Information Protection Law compliance checks, assess personal-information processing risks, and draft compliance document templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwumit](https://clawhub.ai/user/wwumit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Privacy, compliance, legal, and engineering teams use this skill to perform PIPL self-checks, evaluate risks in personal-information processing activities, and generate draft compliance materials for expert review. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: quick-start.py can install Python packages automatically. <br>
Mitigation: Use a virtual environment, review the script before running it, and install dependencies manually when tighter dependency control is required. <br>
Risk: Generated checks, reports, and privacy templates may be incomplete or unreliable as production compliance evidence. <br>
Mitigation: Treat outputs as draft aids and have qualified legal and compliance reviewers validate them against current PIPL requirements and the organization-specific facts. <br>
Risk: The optional API deployment pattern can process sensitive personal data without built-in production controls. <br>
Mitigation: Avoid sensitive data in that deployment unless transport security, access control, logging, retention, and data-handling controls are added. <br>


## Reference(s): <br>
- [PIPL Law Reference](references/pipl-law.md) <br>
- [PIPL Compliance Checklist](references/pipl-checklist.md) <br>
- [China Compliance Checklist](references/cn-checklist.md) <br>
- [Risk Assessment Guide](references/risk-assessment-guide.md) <br>
- [Enforcement Cases](references/enforcement-cases.md) <br>
- [Security Check Guide](SECURITY_CHECK_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated compliance outputs may include JSON, HTML, CSV, Markdown, and plain text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated checks, reports, and templates are draft aids and require legal and security review before operational use.] <br>

## Skill Version(s): <br>
1.1.8 (source: evidence.release, package.json, CHANGELOG, released 2026-03-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
