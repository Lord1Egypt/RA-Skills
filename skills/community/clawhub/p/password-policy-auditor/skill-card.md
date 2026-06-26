## Description: <br>
Audit password policies and authentication configurations for security compliance, including password complexity, storage, rotation policies, MFA coverage, account lockout, and alignment with NIST 800-63, OWASP, and PCI-DSS guidelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and compliance reviewers use this skill to inspect authentication implementations, compare password-policy controls against common standards, and produce remediation guidance before security assessments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit commands and reports may expose sensitive authentication implementation details or secrets. <br>
Mitigation: Run the skill only on systems you are authorized to review, keep raw output private, and redact secrets before sharing reports. <br>
Risk: The optional breached-password example calls a third-party service with a password-derived hash prefix. <br>
Mitigation: Skip the lookup or replace it with an approved offline breach dataset when policy forbids sending password-derived data to third parties. <br>
Risk: Security findings can be misleading if automated searches miss framework-specific configuration or generated code. <br>
Mitigation: Treat generated findings as review inputs and confirm conclusions against the actual authentication code and operational configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/password-policy-auditor) <br>
- [HaveIBeenPwned Pwned Passwords Range API](https://api.pwnedpasswords.com/range/{prefix}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code snippets, guidance] <br>
**Output Format:** [Markdown with audit checklists, command examples, compliance mappings, and remediation plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize sensitive authentication findings; reports should be reviewed and redacted before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
